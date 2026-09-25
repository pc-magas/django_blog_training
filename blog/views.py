from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404

from .models import Article

# Create your views here.
def home(request):
    articles = Article.objects.all().order_by("-id")
    return render(request, "article_list.html",{"articles":articles})

def article(request,slug):
    article = get_object_or_404(Article, slug=slug)

    return render(request, "article.html", {
        "article": article,
    })