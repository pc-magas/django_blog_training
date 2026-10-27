# app_auth/urls.py
from django.urls import path, reverse_lazy
from app_auth import views

urlpatterns = [
    path(
        "complete-registration/<uidb64>/<token>/",
        views.complete_registration,
        name="complete-registration",
    ),
]