from typing import Any, Dict
from django.contrib.auth.models import User
from django.views.generic import ListView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category


class PostDetail(DeleteView):        
    template_name = 'posts/post.html' 
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Post.objects.published(), slug=slug) 


class CategoryList(ListView):    
    template_name = 'posts/category.html'
    paginate_by = 5
        
    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.posts.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context

class AuthorList(ListView):    
    template_name = 'posts/author.html'
    paginate_by = 5
        
    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.posts.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context