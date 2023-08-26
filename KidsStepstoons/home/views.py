from django.shortcuts import render
from posts.models import Post

def home(request):
    return render(
        request=request,
        template_name='home/home.html',
        context={
            "posts": Post.objects.filter(status='p')[:3],
        }
    )
