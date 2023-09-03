from typing import Any, Optional
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from posts.models import Post, Category
from accounts.mixins import (
    FieldsMixin,
    FormValidMixin,
    AuthorAccessMixin,
    SuperuserAccessMixin,
)



class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "dashboard/home.html"


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "dashboard/posts.html"
    
    
    def get_queryset(self):
        
        if self.request.user.is_superuser:
            return Post.objects.all().order_by('-publish')
        else:
            return Post.objects.filter(author=self.request.user).order_by('-publish')


class PostCreateView(LoginRequiredMixin, FieldsMixin, FormValidMixin, CreateView):
    model = Post
    template_name = "dashboard/post_create_update.html"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(AuthorAccessMixin, FieldsMixin, FormValidMixin, UpdateView):
    model = Post
    template_name = "dashboard/post_create_update.html"
    
    def form_valid(self, form):
        # form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(SuperuserAccessMixin, DeleteView):
    model = Post
    template_name = "dashboard/post_delete.html"
    success_url = reverse_lazy("dashboard:posts")