from django import  template
from urls.models import Categories


register = template.Library()


@register.simple_tag()
def get_cat():
    return Categories.objects.all()