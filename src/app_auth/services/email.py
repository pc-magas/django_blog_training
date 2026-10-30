from app_auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

class EmailService:

    def send_registration_email(self, user: User) -> None:

        if user.has_usable_password():
            raise ValueError("User already completed registration.")

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        path = reverse("complete-registration", kwargs={"uidb64": uid, "token": token})
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

    def complete_registration(self,user:User)->None:

        if not user.has_usable_password():
            raise ValueError("User is has not completed registration.")

        login_url = f"{settings.SITE_URL}{reverse('admin:login')}"

        send_mail(
            subject="Welcome aboard",
            message=f"Welcome {user.first_name}! Set your password here:\n{user.email}\n You can login upon your account in:\n{login_url}.",
            recipient_list=[user.email],
            html_message=render_to_string(
                "emails/welcome.html",
                {
                    "user": user,
                    "login_link": login_url ,
                }
            )
        )


    def forgot_password(self,user:User) -> None:

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        path = reverse("complete-registration", kwargs={"uidb64": uid, "token": token})
        link = f"{settings.SITE_URL}{path}"

        send_mail(
            subject="Reset Your Password",
            message=f"Welcome {user.first_name}! Set your password here:\n{link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=render_to_string(
                "emails/reset_password.html", {"user": user, "link": link}
            ),
        )