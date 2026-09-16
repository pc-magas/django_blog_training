from django.db import models
from django.contrib.auth.models import User 
import bleach

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.first_name


class Category(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.TextField()

    def __str__(self):
        return self.name

class Article(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    content=models.TextField()
    slug=models.SlugField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        # TODO: maybe create a common rules for Field Bleaching
        self.content = bleach.clean(
            self.content,
            tags=[
                "p", "br", "strong", "em",
                "ul", "ol", "li",
                "a", "blockquote",
            ],
            attributes={
                "a": ["href", "title", "target", "rel"],
            },
            protocols=["http", "https", "mailto"],
            strip=True,
        )

        super().save(*args, **kwargs)

