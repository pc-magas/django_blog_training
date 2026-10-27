from app_auth.models import User
from django.contrib.auth.models import Group

# TODO: Make an Email Service maybe???
from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.db import transaction

from app_auth.services.group_service import GroupService
from app_auth.services.email import EmailService

from injector import inject



class UserService:

    @inject
    def __init__(self, group_service: GroupService, email_service: EmailService):
        self.__group_service = group_service
        self.__email_service = email_service

    @transaction.atomic
    def complete_registration(self,user:User,password:str)->None:

        if user.has_usable_password():
            raise ValueError("User already completed registration.")

        # set password here

        # Mark user as active
        user.is_active = True

        transaction.on_commit(lambda: self.__email_service.complete_registration(user))


    @transaction.atomic
    def create(self,
               username: str,
               email: str,
               first_name: str,
               last_name: str,
               groups: list[Group],
               bio: str | None = None) -> User:

        user = User()
        user.set_unusable_password()  # important
        user = self.__save(user, username, email, first_name, last_name, groups, bio)
        user.is_active = False

        transaction.on_commit(lambda: self.__email_service.send_registration_emai(user))

        return user

    @transaction.atomic
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
