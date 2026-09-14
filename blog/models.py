from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField()


class Category(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.TextField()

class Article(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.TextField()
    content=models.TextField()
    slug=models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoty = models.ManyToManyField(Category)


