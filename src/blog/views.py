from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404

from .models import Article

# Create your views here.
def home(request):
    articles = Article.objects.all().order_by("-id")
    category = request.GET.get("category")
    if category:
        articles = articles.filter(category__name=category)

    category_id = request.GET.get("category")

    if category_id:
        articles = articles.filter(category=category_id)

    return render(request, "article_list.html",{"articles":articles})

def article(request,slug):
    article = get_object_or_404(Article, slug=slug)

    return render(request, "article.html", {
        "article": article,
    })