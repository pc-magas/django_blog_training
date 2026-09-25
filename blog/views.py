from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Article

# Create your views here.
def home(request):
    articles = Article.objects.all().order_by("-id")

    paginator = Paginator(articles, 10)  # 10 articles per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "article_list.html",{"articles":articles})

def article(request,id):
    article = Article.objects.get(id=id)