from django.urls import path
from .views import post, category

app_name = 'posts'
urlpatterns = [
    path('post/<slug:slug>', post, name='post'),
    path('category/<slug:slug>', category, name='category')
]
