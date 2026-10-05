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

