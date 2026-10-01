from django.contrib import admin
from django.contrib.admin import AdminSite
from django.core.exceptions import ValidationError

from app_auth.container import Container
from dependency_injector.wiring import Provide, inject


from app_auth.models import User
from app_auth.services.group_service import GroupService
from app_auth.services.save.user import UserService


# Register your models here.

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    change_form_template = "admin/register_user.html"

    list_display = ("username", "email", "first_name", "last_name")

    @inject
    def __init__(self,
                 model,
                 admin_site: AdminSite,
                 group_service: GroupService = Provide[Container.group_service],
                 user_service: UserService = Provide[Container.user_service],
    ):
        super().__init__(model, admin_site)
        self.__group_service = group_service
        self.__user_service = user_service

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

        return self.__group_service.user_can_manage_groups(request.user, set(obj.groups.values_list("name", flat=True)))

    def has_delete_permission(self, request, obj=None):
        # Don't forget this one: it bypasses your change rules otherwise.
        if obj is not None and obj.pk == request.user.pk:
            return False

        if not request.user.has_perm('auth.delete_user'):
            return False

        if obj is None:
            return True

        return self.__group_service.user_can_manage_groups(request.user, set(obj.groups.values_list("name", flat=True)))

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
        managed_roles = self.__group_service.get_managed_groups(list(user_groups))

        qs = super().get_queryset(request)

        if managed_roles:
            # filter roles
            return qs.filter()

        return qs

    def save_model(self, request, obj, form, change):
        # Check whether current user can manage roles
        groups = form.cleaned_data.get("groups")

        if not self.__group_service.user_can_manage_groups(request.user, set(groups)):
            raise ValidationError(
                "You do not have permission to manage these groups."
            )

        if change:
            self.__user_service.update(
                user=obj,
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                roles=groups
            )

            return

        self.__user_service.create(
            user=obj,
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            roles=groups
        )
        # Save User
