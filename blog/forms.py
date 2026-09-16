from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].widget.can_add_related = False
        self.fields["category"].widget.can_change_related = False
        self.fields["category"].widget.can_delete_related = False
        self.fields["category"].widget.can_view_related = False

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
            }),
        }

        labels = {
            'title': '',
            'content': '',
        }