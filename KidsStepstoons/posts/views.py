from django.shortcuts import render, get_object_or_404
from .models import Post, Category

def post(request, slug):
    return render(
        request=request,
        template_name='posts/post.html',
        context={
            "post": get_object_or_404(Post, slug=slug, status='p')
        }
    )


def category(request, slug):
    return render(
        request=request,
        template_name='posts/category.html',
        context={
            "category": get_object_or_404(Category, slug=slug, status=True)
        }
    )
