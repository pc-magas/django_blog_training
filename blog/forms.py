from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ["title","slug", "content", "category"]

        widgets = {
            "content": forms.Textarea(attrs={
                "id": "article-content",
                "placeholder": "Article Content",
            }),
            "title": forms.TextInput(attrs={
                "placeholder": "Place Article Title Here",
            })
        }

        labels = {
            'title': '',
            'content': '',
        }