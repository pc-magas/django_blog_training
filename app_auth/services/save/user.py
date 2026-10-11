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
from injector import inject

class UserService:

    @inject
    def __init__(self, group_service: GroupService):
        self.__group_service = group_service


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

        # TODO: Make an Email Service for sending the emails towards the user
        transaction.on_commit(lambda: self.__send_registration_email(user))

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

    def resend_registration_email(self, user: User) -> None:
        if user.has_usable_password():
            raise ValueError("User already completed registration.")
        self.__send_registration_email(user)

    def __send_registration_email(self, user: User) -> None:

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        path = reverse("complete_registration", kwargs={"uidb64": uid, "token": token})
        link = f"{settings.SITE_URL}{path}"

        send_mail(
            subject="Complete your registration",
            message=f"Welcome {user.first_name}! Set your password here:\n{link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=render_to_string(
                "emails/complete_registration.html", {"user": user, "link": link}
            ),
        )

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
