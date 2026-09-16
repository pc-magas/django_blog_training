from django.contrib import admin
from .models import Author, Category, Article
from .forms import ArticleForm


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    
    form = ArticleForm
    change_form_template = "admin/article.html"

    list_display = ("title", "author", "slug")
    list_filter = ("category", "author")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
