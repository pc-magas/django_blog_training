from app_auth.models import User
from django.contrib.auth.models import Group

from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from app_auth.services.group_service import GroupService
from app_auth.services.email import EmailService

from injector import inject


class UserService:

    @inject
    def __init__(self, group_service: GroupService, email_service: EmailService):
        self.__group_service = group_service
        self.__email_service = email_service

    def get_user_pending_for_registration_complete(self, uidb64: str, token: str) -> User:

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,):
            return None

        if user.has_usable_password():
            return None

        if default_token_generator.check_token(user, token):
            return None

        return user

    @transaction.atomic
    def complete_registration(self, user: User, token: str, password: str) -> None:

        if user.has_usable_password():
            raise ValueError("User already completed registration.")

        if password == "":
            raise ValueError("Password cannot be empty.")

        user.set_password(password)
        user.is_active = True

        user.save(update_fields=["password", "is_active"])

        transaction.on_commit(lambda: self.__email_service.complete_registration(user))

    @transaction.atomic
    def create(self,
               email: str,
               first_name: str,
               last_name: str,
               groups: list[Group],
               bio: str | None = None) -> User:

        try:
            user = User.objects.get(email=email)

            if user.has_usable_password():
                raise ValueError("User already registered.")

        except User.DoesNotExist:
            user = None

        if user == None:
            user = User()

        user.is_active = False
        user.set_unusable_password()  # important
        user = self.__save(user, email, first_name, last_name, groups, bio)

        transaction.on_commit(lambda: self.__email_service.send_registration_email(user))

        return user

    @transaction.atomic
    def update(self,
               user: User,
               email: str,
               first_name: str,
               last_name: str,
               groups: list[str | Group],
               bio: str | None = None) -> User:

        user = self.__save(user, email, first_name, last_name, groups, bio)

        return user

    def __save(self,
               user: User,
               email: str,
               first_name: str,
               last_name: str,
               groups: list[str | Group],
               bio: str | None = None
               ) -> User:

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

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
