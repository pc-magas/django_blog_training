from django.contrib import admin
from app_auth.models import User
from app_auth.utils.policy_utils import PolicyUtils

# Register your models here.

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    change_form_template = "admin/register_user.html"

    list_display = ("username", "email", "first_name", "last_name")

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.has_perm("app_auth.add_user")

    def has_change_permission(self, request, obj=None):

        if obj is not None and obj.pk == request.user.pk:
            # User is editing their own profile
            return True

        if not request.user.has_perm('auth.change_user'):
            return False

        if obj is None:
            return True

        return PolicyUtils.user_can_manage_roles(request.user, set(obj.groups.values_list("name", flat=True)))

    def has_delete_permission(self, request, obj=None):
        # Don't forget this one: it bypasses your change rules otherwise.
        if obj is not None and obj.pk == request.user.pk:
            return False

        if not request.user.has_perm('auth.delete_user'):
            return False

        if obj is None:
            return True

        return PolicyUtils.user_can_manage_roles(request.user, set(obj.groups.values_list("name", flat=True)))

    def has_module_permission(self, request, obj=None):

        if obj is None:
            return True

        if obj is not None and obj.pk == request.user.pk:
            return True

        return (
                request.user.has_perm('auth.change_user') or
                request.user.has_perm('auth.add_user') or
                request.user.has_perm('auth.delete_user')
        )

    def has_view_permission(self, request, obj=None):

        if request.user.is_superuser:
            return True

        if obj is not None and obj.pk == request.user.pk:
            return True

        if obj is None:
            return True

        return (
                request.user.has_perm('auth.change_user') or
                request.user.has_perm('auth.add_user') or
                request.user.has_perm('auth.delete_user')
        )

    def get_queryset(self, request):

        user_groups = request.user.groups.all().values_list("name", flat=True)
        managed_roles = PolicyUtils.get_managed_roles(list(user_groups))

        qs = super().get_queryset(request)

        if managed_roles:
            # filter roles
            return qs.filter()

        return qs
