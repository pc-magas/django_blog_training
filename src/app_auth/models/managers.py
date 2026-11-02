rom django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    @inject
    def __init__(self, user_service: UserService = None):
        super().__init__()
        self.__user_service = user_service

    def create_user(self, email, password=None, **extra_fields):
        return self.__user_service.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            groups=groups,
            bio=bio
        )

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_superuser(email=email,password=password)