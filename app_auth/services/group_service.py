from django.contrib.auth.models import AbstractUser, Group
from app_auth.services.policy_service import PolicyService


class GroupService:

    def __init__(self, policy_service:PolicyService ):
        self.__policy_service = policy_service

    def get_managed_groups(self, groups: list) -> list:
        aggregated_policy = self.__policy_service.get_current_policy_aggregated()
        aggregated_groups = set()
        for group in groups:

            if not group in aggregated_policy:
                continue

            # Aggregated Policy has manage_groups
            group_managing_roles = aggregated_policy[group]['manage_groups']
            aggregated_groups.update(group_managing_roles)

        return list(aggregated_groups)

    def user_can_manage_groups(self, user: AbstractUser, target_groups: set) -> bool:
        user_groups = user.groups.all().values_list("name", flat=True)
        managed_groups = self.get_managed_groups(user_groups)

        if not managed_groups:
            return True

        return bool(target_groups & set(managed_groups))

    def get_group_str(self, role: str | Group):

        if isinstance(role, str):
            return role

        return role.name

    def get_groups(self, roles: list[str | Group]) -> list[Group]:
        final_roles = []
        for role in roles:
            if isinstance(role, str):
                role=Group.objects.get(name=role)

            final_roles.append(role)

        return final_roles

    def user_can_be_superuser(self, groups: list[str|Group]) -> bool:
        policy = self.__policy_service.get_current_policy_aggregated()

        for role in groups:
            role_policy = policy[self.get_group_str(role)]

            if role_policy['is_superuser']:
                return True

        return False

    def user_can_be_staff(self, groups: list[str|Group]) -> bool:

        policy = self.__policy_service.get_current_policy_aggregated()

        for role in groups:
            role_policy = policy[self.get_group_str(role)]

            # Logic indicating whether is superuser is placed elsewhere
            if role_policy['is_staff']:
                return True

        return False