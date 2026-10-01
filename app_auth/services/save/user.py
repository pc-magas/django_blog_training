from app_auth.models import User
from django.contrib.auth.models import Group

from app_auth.services.group_service import GroupService

class UserService:

    def __init__(self, group_service: GroupService):
        self.__group_service = group_service

    def create(self,
               username: str,
               email: str,
               first_name: str,
               last_name: str,
               roles: list[str | Group],
               bio: str | None = None) -> User:
        user = self.__save(User.objects.create(), username, email, first_name, last_name, roles,bio)
        # TODO send email to user
        return user

    def update(self,
               user: User,
               username: str,
               email: str,
               first_name: str,
               last_name: str,
               roles: list[str | Group],
               bio: str|None = None) -> User:
        user = self.__save(user, username, email, first_name, last_name, roles,bio)
        return user

    def __save(self,
               user: User,
               username: str,
               email: str,
               first_name: str,
               last_name: str,
               roles: list[str | Group],
               bio: str|None = None
               ) -> User:
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        is_superuser = self.__group_service.user_can_be_superuser(roles)
        is_staff = is_superuser

        if not is_superuser:
            is_staff = self.__group_service.user_can_be_staff(roles)

        user.is_superuser = is_superuser
        user.is_staff = is_staff

        user.groups = self.__group_service.get_groups(roles)

        user.save()
        return user
