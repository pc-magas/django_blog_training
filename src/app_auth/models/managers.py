from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.apps import apps

from app_auth.auth.groups import ADMIN
from app_auth.services.save.user import UserService

class UserManager(BaseUserManager):

    @property
    def __user_service(self) -> UserService:
        injector = apps.get_app_config("django_injector").injector
        return injector.get(UserService)

    def create_user(self, email, password=None, **extra_fields):
        return self.__user_service.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            groups=groups,
            bio=bio
        )

    def create_superuser(self, email, password=None, **user_data):
        
        if password==None or password=="":
            return self.__user_service.create_user(email=email,first_name="",last_name="",groups=[ADMIN])
        
        return self.__user_service.create_superuser_with_password(email=email,first_name="",last_name="",password=password)