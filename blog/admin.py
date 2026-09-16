from django.contrib import admin
from .models import Category, Article
from .forms import ArticleForm

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

    def has_add_permission(self, request):
        return request.user.has_perm("blog.create_article")

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm("blog.edit_article")

