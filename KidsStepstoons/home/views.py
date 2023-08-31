from django.shortcuts import render
from django.db.models import Count
from posts.models import Post, Category

def home(request):
    return render(
        request=request,
        template_name='home/home.html',
        context={
            "posts": Post.objects.published(),
            "categories": Category.objects.annotate(number_of_posts = Count("posts")).filter(status=True)
        }
    )