from django.contrib import admin
from .models import Category, Article
from .forms import ArticleForm

import blog.auth.groups

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
        return request.user.has_perm("blog.add_article") or request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        
        if request.user.is_superuser:
            return True

        if obj is not None and obj.author == request.user:
            return True

        return request.user.has_perm("blog.change_article")

    def has_view_permission(self,request,obj=None):

        if request.user.is_superuser:
            return True
        
        if obj is not None and obj.author == request.user:
            return True
        
        return request.user.has_perm("blog.view_article")
    
    def has_module_permission(self,request,obj=None):

        if request.user.is_superuser:
            return True
        
        return request.user.has_perm("blog.view_article")

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.groups.filter(name=blog.auth.groups.AUTHOR).exists():
            return qs.filter(author=request.user)

        return qs
    
    def save_model(self, request, obj, form, change):
        if not change:  # only when creating a new article
            obj.author = request.user

        super().save_model(request, obj, form, change)