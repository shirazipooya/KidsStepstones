from django.urls import path
from .views import PostDetail, CategoryList, AuthorList

app_name = 'posts'
urlpatterns = [
    path('post/<slug:slug>', PostDetail.as_view(), name='post'),
    path('category/<slug:slug>', CategoryList.as_view(), name='category'),
    path('author/<slug:username>', AuthorList.as_view(), name='author'),
]
