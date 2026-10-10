from django.contrib import admin
from django.apps import apps
from django.http.response import Http404

from app_auth.models import User
from app_auth.services.group_service import GroupService
from app_auth.services.save.user import UserService
from app_auth.forms import UserForm

from common.admin.mixins import CustomAdminFormMixin


# Register your models here.

@admin.register(User)
class AdminUser(CustomAdminFormMixin,admin.ModelAdmin):

    change_form_template = "admin/register_user.html"

    list_display = ("username", "email", "first_name", "last_name")

    @property
    def __group_service(self) -> GroupService:
        injector =  apps.get_app_config("django_injector").injector
        return injector.get(GroupService)

    @property
    def __user_service(self) -> UserService:
        injector = apps.get_app_config("django_injector").injector
        return injector.get(UserService)

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

    def add_view(self, request, form_url="", extra_context=None):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                self.__user_service.create(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    groups=form.cleaned_data["groups"],
                    bio=form.cleaned_data.get("bio"),
                )

                self.message_user(
                    request,
                    "User created successfully.",
                )
        else:
            form = UserForm()

        return self.render_add_change_form(form,request=request,extra_context=extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = self.get_object(request, object_id)

        if obj is None:
            raise Http404

        if request.method == "POST":
            form = UserForm(
                request.POST,
                instance=obj,
            )

            if form.is_valid():
                self.__user_service.update(
                    user=obj,
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    groups=form.cleaned_data["groups"],
                    bio=form.cleaned_data.get("bio"),
                )

                self.message_user(
                    request,
                    "User updated successfully.",
                )
        else:
            form = UserForm(instance=obj)

        return self.render_add_change_form(form, request=request, extra_context=extra_context,change=True)
