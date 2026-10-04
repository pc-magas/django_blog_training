from app_auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "groups","bio"]

