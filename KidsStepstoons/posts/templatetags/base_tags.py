from django import template
from ..models import Category

register = template.Library()

@register.simple_tag
def title(data="همقدم با کودک"):
    return data

@register.inclusion_tag('inc/header.html')
def header():
    return {
        "categories": Category.objects.filter(status=True)
    }