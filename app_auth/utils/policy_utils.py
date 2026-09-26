from django.apps import apps
from importlib import import_module
from app_auth.utils.permission import permission_codename, permission_description
from django.contrib.auth.models import AbstractUser

DEFAULT_GROUP_POLICY = {
    "is_staff":False,
    "is_superuser":False,
    "permissions":{}
}

class PolicyUtils():

    @staticmethod
    def discover_policies():
        """
        Find every installed app containing:

            <app>/auth/policy.py

        The policy module must expose:

            GROUP_PERMISSIONS = {
                "is_staff":True,
                "permissions": {
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

            policy = getattr(module,"POLICY",None)

            if policy is None:
                raise RuntimeError(
                    f"{module_name} exists but does not define "
                    "POLICY."
                )

            app_label = app_config.label

            if app_label in policies:
                raise RuntimeError(
                    f"Duplicate policy for app '{app_label}'."
                )

            policies[app_label] = policy

        return policies

    @staticmethod
    def normalize_permission(permission) -> tuple:
        if isinstance(permission, str):
            return permission, None

        if isinstance(permission, (tuple, list)) and len(permission) >= 1:
            codename = permission_codename(permission)
            description = permission_description(permission)
            return codename, description

        raise ValueError(f"Invalid permission: {permission!r}")


    @staticmethod
    def aggregate_policy(policies)->dict:
        from pprint import pprint

        final_policy = {}

        for group_name, policy in policies.items():
            pprint(policy)

            for group,group_policy in policy.items():
                
                existing_policy = final_policy[group] if group in final_policy is not None else DEFAULT_GROUP_POLICY
                
                if 'manage_groups' not in existing_policy :
                    existing_policy['manage_groups'] = {}

                if 'manage_groups' not in group_policy:
                    group_policy['manage_groups']={}

                if 'is_superuser' not in group_policy:
                    group_policy['is_superuser'] = False

                existing_policy['permissions'] = [permission_codename(p) for p in existing_policy.get("permissions", ())]

                final_group_policy = {
                    "is_staff":existing_policy['is_staff'] or group_policy['is_staff'],
                    "is_superuser":existing_policy['is_superuser'] or group_policy['is_superuser'],
                    "permissions":list(set(existing_policy['permissions'])|set(group_policy['permissions'])),
                    "manage_groups":list(set(existing_policy['manage_groups'])|set(group_policy['manage_groups']))
                }

                final_policy[group]=final_group_policy

        return final_policy
    
    @staticmethod
    def get_current_policy_aggregated():
        policies = PolicyUtils.discover_policies()
        return PolicyUtils.aggregate_policy(policies)

    @staticmethod
    def get_managed_roles(groups: list) -> list:
        aggregated_policy = PolicyUtils.get_current_policy_aggregated()
        aggregated_groups = set()
        for group in groups:

            if not group in aggregated_policy:
                continue

            # Aggregated Policy has manage_groups
            group_managing_roles = aggregated_policy[group]['manage_groups']
            aggregated_groups.update(group_managing_roles)

        return list(aggregated_groups)

    @staticmethod
    def user_can_manage_roles( user: AbstractUser, target_roles: set) -> bool:
        user_groups = user.groups.all().values_list("name", flat=True)
        managed_roles = PolicyUtils.get_managed_roles(user_groups)

        if not managed_roles:
            return True

        return bool(target_roles & set(managed_roles))