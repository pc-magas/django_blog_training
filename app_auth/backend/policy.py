# articles/auth/backend.py

from django.contrib.auth.backends import BaseBackend

from .policy import GROUP_PERMISSIONS


class PolicyBackend(BaseBackend):

    def has_perm(self, user, perm, obj=None):
        if not user.is_active:
            return False

        app_label, codename = perm.split(".", 1)

        # Only handle permissions belonging to this app.
        if app_label != "articles":
            return False

        for group in user.groups.all():
            permissions = GROUP_PERMISSIONS.get(group.name, set())

            for permission in permissions:
                if permission[0] == codename:
                    return True

        return False