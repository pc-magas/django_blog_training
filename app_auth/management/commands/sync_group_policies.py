from importlib import import_module

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from django.contrib.auth.models import Group, Permission

from pprint import pprint

class Command(BaseCommand):
    help = "Synchronize Django Groups and Permissions from app auth/policy.py files."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show the changes without applying them.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        policies = self.discover_policies()
        
        if not policies:
            self.stdout.write(
                self.style.WARNING("No auth/policy.py files were found.")
            )
            return

        self.stdout.write("Discovered policies:")
        self.__print_policies(policies)

        final_policy = self.aggregate_policy(policies)

        self.stdout.write("\n=================")


        with transaction.atomic():
            self.stdout.write("Syncing groups")
            self.sync_groups(final_policy)


        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("Policy synchronization completed.")
        )

    def sync_groups(self,policy):
        db_groups = Group.objects.all()
        
        existing_policies=[]

        for db_group in db_groups:
            #db_group.name
            if (db_group.name in policy):
                # update permission
                self.sync_group_permissions(policy[db_group.name],db_group)
                db_group.save()
                existing_policies.append(db_group.name)
            else:
                db_group.permissions.clear()
                db_group.delete()
        

        new_groups = set(policy.keys()) - set(existing_policies)

        for group_name in new_groups:
            # Create the group
            db_group = Group.objects.create(name=group_name)
            self.sync_group_permissions(policy[db_group.name],db_group)
            db_group.save()

    def sync_group_permissions(self,permissions:list,group:Group):
        
        permissions = set(map(lambda p: self.permission_codename(p), permissions))
        db_permissions = set(group.permissions.values_list("codename", flat=True))

        # get permissions in db but not permissions list
        to_remove = db_permissions - permissions

        for permission_to_remove in to_remove:
            self.stdout.write(f"Removing Permission {permission_to_remove} from group {group.name}")

            try:
                permission = group.permissions.get(codename=permission_to_remove)
                group.permissions.remove(permission)
            except Permission.DoesNotExist:
                self.stderr.write(f"Permission {permission_to_remove} not found skipping removal from group {group.name}")
                pass


        to_add = permissions - db_permissions
        for permission_to_add in to_add:
            self.stdout.write(f"Adding Permission {permission_to_add} into group {group.name}")
            
            try:
                # Persmission adding or removal is performed via migrations
                permission = Permission.objects.get(codename=permission_to_add)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stderr.write(f"Permission {permission_to_add} not found skipping adding into group {group.name}")
                pass


    def __print_policies(self,policies):
        for app_label, group_permissions in policies.items():
            self.stdout.write(f"++ APP: {app_label} ++")
            
            for group_name, permissions in group_permissions.items():
                self.stdout.write(f"GROUP: {group_name}")
                
                for permission in permissions:
                    self.stdout.write(f"\t{permission[0]} : {permission[1]}")
            

                

              
    # ------------------------------------------------------------------
    # Policy discovery
    # ------------------------------------------------------------------

    def discover_policies(self):
        """
        Find every installed app containing:

            <app>/auth/policy.py

        The policy module must expose:

            GROUP_PERMISSIONS = {
                "group_name": {
                   ("permission_name","permission_description"),
                    ...
                }
            }
        """

        policies = {}

        for app_config in apps.get_app_configs():
            module_name = f"{app_config.name}.auth.policy"

            if module_name.startswith("django"):
                continue

            try:
                module = import_module(module_name)
            except ModuleNotFoundError as exc:
                continue

            group_permissions = getattr(
                module,
                "GROUP_PERMISSIONS",
                None,
            )

            if group_permissions is None:
                raise CommandError(
                    f"{module_name} exists but does not define "
                    "GROUP_PERMISSIONS."
                )

            app_label = app_config.label

            if app_label in policies:
                raise CommandError(
                    f"Duplicate policy for app '{app_label}'."
                )

            policies[app_label] = group_permissions

        return policies

    # ------------------------------------------------------------------
    # Convert policies into:
    #
    # {
    #     "author": {
    #         "create_article",
    #         "edit_article",
    #     },
    # }
    # ------------------------------------------------------------------

    def aggregate_policy(self, policies):
        desired_groups = {}

        for app_label, group_permissions in policies.items():
            for group_name, permissions in group_permissions.items():

                if group_name not in desired_groups:
                    desired_groups[group_name] = set()

                for permission in permissions:
                    codename = self.permission_codename(permission)

                    permission_id = f"{codename}"

                    desired_groups[group_name].add(permission_id)

        return desired_groups

    # ------------------------------------------------------------------
    # Permission definition handling
    # ------------------------------------------------------------------

    @staticmethod
    def permission_codename(permission):
        """
        Supports both:

            "create_article"

        and:

            (
                "create_article",
                "Can create article",
            )
        """

        if isinstance(permission, str):
            return permission

        if isinstance(permission, (tuple, list)) and permission:
            return permission[0]

        raise CommandError(
            f"Invalid permission definition: {permission!r}"
        )

    

    