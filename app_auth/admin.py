from django.contrib import admin
from app_auth.models import User
# Register your models here.

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display=("username","email","first_name","last_name")
    pass
