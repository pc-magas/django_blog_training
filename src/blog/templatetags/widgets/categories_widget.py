from django import template

register = template.Library()

@register.inclusion_tag("widgets/categories_sidebar.html", takes_context=True)
def categories_widget(context):
    from blog.models import Category
    categories = Category.objects.order_by("name")
    return {
        "categories": categories,
    }