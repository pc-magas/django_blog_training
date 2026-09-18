from django.db import models
from django.contrib.auth.models import Group,AbstractUser


# Create your models here.
class User(AbstractUser):
    bio = models.TextField()

    def __str__(self):
        return self.first_name+' '+self.last_name

class Author(Group):
    class Meta:
        proxy=True
        permissions=[("create_article","User can create article"),("edit_article","Edit Article")]

class Publisher(Group):
    class Meta:
        proxy=True
        permissions=[("edit_article","Edit Article")]