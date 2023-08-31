from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from posts.models import Post, Category



def home(request):
    return render(request, "dashboard/home.html")

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "dashboard/posts.html"
    
    
    def get_queryset(self):
        
        if self.request.user.is_superuser:
            return Post.objects.all().order_by('-publish')
        else:
            return Post.objects.filter(author=self.request.user).order_by('-publish')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['author', 'title', 'slug', 'category', 'body', 'thumbnail', 'publish', 'status']
    template_name = "dashboard/post_create_update.html"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)