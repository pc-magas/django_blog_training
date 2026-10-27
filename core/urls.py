"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.auth import views as auth_views

admin.site.site_header = getattr(
    settings, "ADMIN_SITE_HEADER", "Django Administration"
)
admin.site.index_title = getattr(
    settings, "ADMIN_INDEX_TITLE", "Site administration"
)
admin.site.site_title = getattr(
    settings, "ADMIN_SITE_TITLE", "Django site admin"
)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views

# Preserve admin branding
admin.site.site_header = getattr(
    settings, "ADMIN_SITE_HEADER", "Django Administration"
)
admin.site.index_title = getattr(
    settings, "ADMIN_INDEX_TITLE", "Site administration"
)
admin.site.site_title = getattr(
    settings, "ADMIN_SITE_TITLE", "Django site admin"
)

urlpatterns = [
    # Password reset URLs first
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

    # Keep the original admin site
    path("admin/", admin.site.urls),

    path("", include("app_auth.urls")),
    path("", include("blog.urls")),
]
