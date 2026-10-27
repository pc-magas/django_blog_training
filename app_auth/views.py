# app_auth/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages

from injector import inject

from services.save.user import UserService

User = get_user_model()

@inject
def complete_registration(request, uidb64, token,user_service: UserService):
    """
    Complete registration by validating the token, setting a password,
    and updating additional user fields.
    """

    user = user_service.get_user_pending_for_registration_complete(uidb64,token)
    if user is None:
        return redirect("/")

    # Handle GET and POST
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)

        if form.is_valid():

            if form.cleaned_data["new_password1"] != form.cleaned_data["new_password2"]:
                return render(
                    request,
                    "app_auth/complete_registration.html",
                    {
                        "form": form,
                        "validlink": False,
                        "title": "Complete Registration",
                        "desc": "Set your password and complete your profile.",
                    },
                )

            user_service.complete_registration(
                user=user,
                password=form.cleaned_data["new_password1"],
            )

            messages.success(
                request,
                "Registration completed successfully. You can now log in.",
            )

            return redirect("admin:login")

    else:
        form = SetPasswordForm(user)

    return render(
        request,
        "app_auth/complete_registration.html",
        {
            "form": form,
            "validlink": True,
            "title": "Complete Registration",
            "desc": "Set your password and complete your profile.",
        },
    )