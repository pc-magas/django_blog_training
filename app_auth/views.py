# app_auth/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.db import transaction


User = get_user_model()


def complete_registration(request, uidb64, token):
    """
    Complete registration by validating the token, setting a password,
    and updating additional user fields.
    """

    validlink = False
    if not validlink:
        return render(
            request,
            "app_auth/complete_registration.html",
            {"validlink": False},
        )

    # Handle GET and POST
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)

        if form.is_valid():

            # TODO: Use save/user

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