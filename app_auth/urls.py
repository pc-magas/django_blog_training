# app_auth/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "complete-registration/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="app_auth/complete_registration.html",
            success_url="/login/",          # or reverse_lazy("login")
        ),
        name="complete_registration",
    ),
]