from django.db import models
from django.conf import settings
from common.services.xss_sanitizer import xss_sanitize_html

import bleach

class Category(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Article(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    content=models.TextField()
    slug=models.SlugField(unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        # TODO: maybe create a common rules for Field Bleaching
        self.content = xss_sanitize_html(self.content)

        super().save(*args, **kwargs)