from django.contrib import admin
from app_auth.models import User
from app_auth.utils.policy_aggregator import PolicyAggregator

# Register your models here.

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")

    def __get_managed_roles(self,groups: list) -> list:
        aggregated_policy = PolicyAggregator.get_current_policy_aggregated()
        aggregated_groups = set()
        for group in groups:

            if not group in aggregated_policy:
                continue

            # Aggregated Policy has manage_groups
            group_managing_roles = aggregated_policy[group]['manage_groups']
            aggregated_groups.update(group_managing_roles)

        return list(aggregated_groups)

    def __user_can_manage_roles(self, user: User, target_roles: set) -> bool:
        user_groups = user.groups.all().values_list("name", flat=True)
        managed_roles = self.__get_managed_roles(user_groups)

        if not managed_roles :
            return True

        return bool(target_roles & set(managed_roles))

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

        return self.__user_can_manage_roles(request.user, set(obj.groups.values_list("name", flat=True)))

    def has_delete_permission(self, request, obj=None):
        # Don't forget this one: it bypasses your change rules otherwise.
        if obj is not None and obj.pk == request.user.pk:
            return False

        if not request.user.has_perm('auth.delete_user'):
            return False

        if obj is None:
            return True

        return self.__user_can_manage_roles(request.user, set(obj.groups.values_list("name", flat=True)))

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
        managed_roles = self.__get_managed_roles(list(user_groups))

        qs = super().get_queryset(request)

        if managed_roles:
            # filter roles
            return qs.filter()

        return qs
