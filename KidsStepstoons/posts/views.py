from typing import Any, Dict
from account.models import User
from django.views.generic import ListView, DeleteView, DetailView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category
from account.mixins import AuthorAccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType


class PostDetail(DetailView):        
    template_name = 'posts/post.html' 
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post.objects.published(), slug=slug)
        
        ip_address = self.request.user.ip_address
        
        if ip_address not in post.hits.all():
            post.hits.add(ip_address)
        
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_type_id = ContentType.objects.get(app_label="posts", model="post").id
        context['new_posts'] = Post.objects.published().order_by('-publish')[:10]
        context['pop_posts'] = Post.objects.published().annotate(
            count=Count(
                'hits', 
                filter=Q(posthit__created__gte=datetime.today() - timedelta(days=30))
            )
        ).order_by('-count', '-publish')[:10]
        context['hot_posts'] = Post.objects.published().annotate(
            count=Count(
                'comments', 
                filter=Q(comments__posted__gte=datetime.today() - timedelta(days=30) and Q(comments__content_type_id=content_type_id))
            )
        ).order_by('-count', '-publish')[:10]
        
        return context



class PostPreview(AuthorAccessMixin, DetailView):
    template_name = 'posts/post.html'
     
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Post, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_type_id = ContentType.objects.get(app_label="posts", model="post").id
        context['new_posts'] = Post.objects.published().order_by('-publish')[:10]
        context['pop_posts'] = Post.objects.published().annotate(
            count=Count(
                'hits', 
                filter=Q(posthit__created__gte=datetime.today() - timedelta(days=30))
            )
        ).order_by('-count', '-publish')[:10]
        context['hot_posts'] = Post.objects.published().annotate(
            count=Count(
                'comments', 
                filter=Q(comments__posted__gte=datetime.today() - timedelta(days=30) and Q(comments__content_type_id=content_type_id))
            )
        ).order_by('-count', '-publish')[:10]
        
        return context



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
        content_type_id = ContentType.objects.get(app_label="posts", model="post").id
        context['new_posts'] = Post.objects.published().order_by('-publish')[:10]
        context['pop_posts'] = Post.objects.published().annotate(
            count=Count(
                'hits', 
                filter=Q(posthit__created__gte=datetime.today() - timedelta(days=30))
            )
        ).order_by('-count', '-publish')[:10]
        context['hot_posts'] = Post.objects.published().annotate(
            count=Count(
                'comments', 
                filter=Q(comments__posted__gte=datetime.today() - timedelta(days=30) and Q(comments__content_type_id=content_type_id))
            )
        ).order_by('-count', '-publish')[:10]
        
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
        content_type_id = ContentType.objects.get(app_label="posts", model="post").id
        context['new_posts'] = Post.objects.published().order_by('-publish')[:10]
        context['pop_posts'] = Post.objects.published().annotate(
            count=Count(
                'hits', 
                filter=Q(posthit__created__gte=datetime.today() - timedelta(days=30))
            )
        ).order_by('-count', '-publish')[:10]
        context['hot_posts'] = Post.objects.published().annotate(
            count=Count(
                'comments', 
                filter=Q(comments__posted__gte=datetime.today() - timedelta(days=30) and Q(comments__content_type_id=content_type_id))
            )
        ).order_by('-count', '-publish')[:10]
        
        return context


class SpecialList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/special.html'
    paginate_by = 5
    
    
    def get_queryset(self):
        return Post.objects.filter(is_special=True).order_by('-publish')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_type_id = ContentType.objects.get(app_label="posts", model="post").id
        context['new_posts'] = Post.objects.published().order_by('-publish')[:10]
        context['pop_posts'] = Post.objects.published().annotate(
            count=Count(
                'hits', 
                filter=Q(posthit__created__gte=datetime.today() - timedelta(days=30))
            )
        ).order_by('-count', '-publish')[:10]
        context['hot_posts'] = Post.objects.published().annotate(
            count=Count(
                'comments', 
                filter=Q(comments__posted__gte=datetime.today() - timedelta(days=30) and Q(comments__content_type_id=content_type_id))
            )
        ).order_by('-count', '-publish')[:10]
        
        return context



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
        content_type_id = ContentType.objects.get(app_label="posts", model="post").id
        context['new_posts'] = Post.objects.published().order_by('-publish')[:10]
        context['pop_posts'] = Post.objects.published().annotate(
            count=Count(
                'hits', 
                filter=Q(posthit__created__gte=datetime.today() - timedelta(days=30))
            )
        ).order_by('-count', '-publish')[:10]
        context['hot_posts'] = Post.objects.published().annotate(
            count=Count(
                'comments', 
                filter=Q(comments__posted__gte=datetime.today() - timedelta(days=30) and Q(comments__content_type_id=content_type_id))
            )
        ).order_by('-count', '-publish')[:10]
        
        return context
