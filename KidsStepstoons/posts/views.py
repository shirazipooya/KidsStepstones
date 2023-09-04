from typing import Any, Dict
from account.models import User
from django.views.generic import ListView, DeleteView, DetailView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category
from account.mixins import AuthorAccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class PostDetail(DeleteView):        
    template_name = 'posts/post.html' 
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Post.objects.published(), slug=slug) 


class PostPreview(AuthorAccessMixin, DetailView):
    template_name = 'posts/post.html'
     
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Post, pk=pk)



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


class SpecialList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/special.html'
    paginate_by = 5
    
    
    def get_queryset(self):
        return Post.objects.filter(is_special=True).order_by('-publish')



class SearchList(ListView):    
    template_name = 'posts/search.html'
    paginate_by = 5
        
    def get_queryset(self):
        global search
        search = self.request.GET.get('q')
        return Post.objects.filter(Q(title__icontains=search) | Q(body__icontains=search)).order_by('-publish')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = search
        return context