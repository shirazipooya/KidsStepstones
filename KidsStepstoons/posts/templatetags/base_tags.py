from django import template
from django.utils.safestring import mark_safe
from ..models import Post, Category

register = template.Library()

@register.simple_tag
def title(data="همقدم با کودک"):
    return data

@register.simple_tag
def special_badge(txt="ویژه"):
    
    result = """
        <span class="badge bg-danger"> %s </span>
    """ % txt
    
    return mark_safe(result)

@register.simple_tag
def show_date(date):
    
    result = """
        <i class='bi bi-calendar px-1'></i><span>%s</span>
    """ % date
    
    return mark_safe(result)

@register.simple_tag
def show_name(url, name):
    
    result = """
        <span class="date"></i><a href=%s class=post-meta>%s</a></span>
    """ % (url, name)
    
    return mark_safe(result)

@register.simple_tag
def show_name_date(url, name, date):
    
    result = """
        <i class="bi bi-person-fill px-1"></i><span class="date"></i><a href=%s class=post-meta>%s</a></span>
        <span class="mx-1"></span>
        <i class="bi bi-calendar px-1"></i><span>%s</span>
    """ % (url, name, date)
    
    return mark_safe(result)

@register.simple_tag
def show_name_date_category(url, name, date, cat):
    
    result = """
        <i class="bi bi-person-fill px-1"></i><span class="date"></i><a href=%s class=post-meta>%s</a></span>
        <span class="mx-1"></span>
        <i class="bi bi-calendar px-1"></i><span>%s</span>
        <span class="mx-1"></span>
        <i class="bi bi-tag-fill px-1"></i><span>%s</span>
    """ % (url, name, date, cat[0])
    
    return mark_safe(result)


@register.inclusion_tag('posts/inc/sidebar.html')
def sidebar():
    return {
        "all_posts": Post.objects.published(),
    }
    
@register.inclusion_tag('inc/header.html')
def header():
    return {
        "categories": Category.objects.filter(status=True)
    }
    
@register.inclusion_tag('dashboard/inc/link.html')
def link(request, link_name, content, icon):
    return {
        "request": request,
        "link_name": link_name,
        "link": "dashboard:%s" % link_name,
        "content": content,
        "icon": icon
    }