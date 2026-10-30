from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("article/<slug:slug>/", views.article, name="article"),
]