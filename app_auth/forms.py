from app_auth.models import User
from django import forms
from django.contrib.auth.models import Group

class UserForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.instance = instance

        if instance is not None and not self.is_bound:
            self.initial = {
                "username": instance.username,
                "email": instance.email,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "groups": instance.groups.all(),
                "bio": instance.bio,
            }
