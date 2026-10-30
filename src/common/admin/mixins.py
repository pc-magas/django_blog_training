# common/admin/mixins.py

from django.contrib.admin import helpers
from django.template.response import TemplateResponse
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from django.contrib.admin import ModelAdmin

class CustomAdminFormMixin:

    def render_add_change_form(
        self: "ModelAdmin",
        form,
        request,
        form_url="",
        extra_context=None,
        change=False,
        title=None,
    ) -> TemplateResponse:
        fieldsets = [(None, {"fields": list(form.fields)})]

        adminform = helpers.AdminForm(
            form,
            fieldsets,
            prepopulated_fields={},
            readonly_fields=[],
            model_admin=self,
        )

        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "adminform": adminform,
            "errors": helpers.AdminErrorList(form, []),
            "media": self.media + adminform.media,
            "add": not change,
            "change": change,
            "is_popup": False,
            "save_as": False,
            "save_on_top": False,
            "show_save": True,
            "show_save_and_continue": False,
            "show_save_and_add_another": False,
            "show_delete_link": False,
            "show_close": False,
            "has_add_permission": self.has_add_permission(request),
            "has_change_permission": self.has_change_permission(request),
            "has_view_permission": self.has_view_permission(request),
            "has_delete_permission": self.has_delete_permission(request),
            "has_editable_inline_admin_formsets": False,
            "inline_admin_formsets": [],
            "form_url": form_url,
            "title": title or ("Change" if change else "Add"),
            "app_label": self.model._meta.app_label,
            **(extra_context or {}),
        }

        return TemplateResponse(
            request,
            self.change_form_template,
            context,
        )