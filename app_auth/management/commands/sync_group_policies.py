
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from django.contrib.auth.models import Group, Permission
from app_auth.utils.policy_utils import PolicyUtils
from app_auth.utils.permission import permission_codename, permission_description

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

        policies = PolicyUtils.discover_policies()
        
        if not policies:
            self.stdout.write(
                self.style.WARNING("No auth/policy.py files were found.")
            )
            return

        self.stdout.write("Discovered policies:")
        self.__print_policies(policies)

        final_policy = PolicyUtils.aggregate_policy(policies)

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

        from pprint import pprint

        for db_group in db_groups:
            group_permissions = policy[db_group.name]['permissions']
            #db_group.name
            if (db_group.name in policy):
                # update permission
                self.sync_group_permissions(group_permissions,db_group)
                db_group.save()
                existing_policies.append(db_group.name)
            else:
                db_group.permissions.clear()
                db_group.delete()
        

        new_groups = set(policy.keys()) - set(existing_policies)

        for group_name in new_groups:
            group_permissions = policy[group_name]['permissions']

            # Create the group
            db_group = Group.objects.create(name=group_name)
            self.sync_group_permissions(group_permissions,db_group)
            db_group.save()

    def sync_group_permissions(self,permissions:list,group:Group):
        
        permissions = set(map(lambda p: permission_codename(p), permissions))
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
                # Permission adding or removal is performed via migrations
                permission = Permission.objects.get(codename=permission_to_add)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stderr.write(f"Permission {permission_to_add} not found skipping adding into group {group.name}")
                pass

    def __print_policies(self,policies):
        for app_label, policy in policies.items():
            self.stdout.write(f"++ APP: {app_label} ++")
            
            for group_name, group_policy in policy.items():
                self.stdout.write(f"GROUP: {group_name}")
                for permission in group_policy['permissions']:
                    self.stdout.write(f"\t{permission_codename(permission)} : {permission_description(permission)}")
