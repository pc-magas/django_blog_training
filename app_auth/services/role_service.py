from django.contrib.auth.models import AbstractUser
from app_auth.services.policy_service import PolicyService

class RoleService:

    def __init__(self, policy_service:PolicyService ):
        self.__policy_service = policy_service

    def get_managed_roles(self,groups: list) -> list:
        aggregated_policy = self.__policy_service.get_current_policy_aggregated()
        aggregated_groups = set()
        for group in groups:

            if not group in aggregated_policy:
                continue

            # Aggregated Policy has manage_groups
            group_managing_roles = aggregated_policy[group]['manage_groups']
            aggregated_groups.update(group_managing_roles)

        return list(aggregated_groups)

    def user_can_manage_roles(self, user: AbstractUser, target_roles: set) -> bool:
        user_groups = user.groups.all().values_list("name", flat=True)
        managed_roles = self.get_managed_roles(user_groups)

        if not managed_roles:
            return True

        return bool(target_roles & set(managed_roles))