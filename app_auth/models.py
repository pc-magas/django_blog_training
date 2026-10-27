from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'email'
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    username = None

    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.first_name+' '+self.last_name
