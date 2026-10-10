from app_auth.models import User
from django.contrib.auth.models import Group

# TODO: Make an Email Service maybe???
from django.core.mail import send_mail


from app_auth.services.group_service import GroupService
from injector import inject
from django.db import transaction

class UserService:

    @inject
    def __init__(self, group_service: GroupService):
        self.__group_service = group_service


    def create(self,
               username: str,
               email: str,
               first_name: str,
               last_name: str,
               groups: list[Group],
               bio: str | None = None) -> User:

        user = self.__save(User(), username, email, first_name, last_name, groups, bio)

        # TODO: Make an Email Service for sending the emails towards the user
        send_mail(
            "Activate your account",
            "Activate your account",
            "from@example.com",
            [user.email],
        )

        return user

    def update(self,
               user: User,
               username: str,
               email: str,
               first_name: str,
               last_name: str,
               groups: list[str | Group],
               bio: str|None = None) -> User:
        user = self.__save(user, username, email, first_name, last_name, groups, bio)
        return user

    @transaction.atomic
    def __save(self,
               user: User,
               username: str,
               email: str,
               first_name: str,
               last_name: str,
               groups: list[str | Group],
               bio: str|None = None
               ) -> User:

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        # TODO: XSS SANITIZE
        user.bio = bio

        is_superuser = self.__group_service.user_can_be_superuser(groups)
        is_staff = is_superuser

        if not is_superuser:
            is_staff = self.__group_service.user_can_be_staff(groups)

        user.is_superuser = is_superuser
        user.is_staff = is_staff

        user.save()

        group_models = self.__group_service.get_groups(groups)
        user.groups.set(group_models)

        user.save()

        return user
