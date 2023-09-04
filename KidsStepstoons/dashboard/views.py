from typing import Any, Dict, Optional
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import User
from .forms import ProfileForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from posts.models import Post, Category
from account.mixins import (
    FieldsMixin,
    FormValidMixin,
    AuthorAccessMixin,
    SuperuserAccessMixin,
    AuthorsAccessMixin
)



class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "dashboard/home.html"


class PostListView(AuthorsAccessMixin, ListView):
    model = Post
    template_name = "dashboard/posts.html"
    
    
    def get_queryset(self):
        
        if self.request.user.is_superuser:
            return Post.objects.all().order_by('-publish')
        else:
            return Post.objects.filter(author=self.request.user).order_by('-publish')


class PostCreateView(AuthorsAccessMixin, FieldsMixin, FormValidMixin, CreateView):
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



class Profile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'dashboard/profile.html'
    success_url = reverse_lazy("dashboard:profile")
    
    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)
    
    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update(
            {'user': self.request.user}
        )
        return kwargs