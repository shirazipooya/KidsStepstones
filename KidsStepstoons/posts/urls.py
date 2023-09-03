from django.urls import path
from .views import PostDetail, CategoryList, AuthorList, PostPreview, SpecialList, SearchList

app_name = 'posts'
urlpatterns = [
    path('post/<slug:slug>', PostDetail.as_view(), name='post'),
    path('preview/<int:pk>', PostPreview.as_view(), name='preview'),
    path('category/<slug:slug>', CategoryList.as_view(), name='category'),
    path('special/', SpecialList.as_view(), name='special'),
    path('author/<slug:username>', AuthorList.as_view(), name='author'),
    path('search/', SearchList.as_view(), name='search'),
    path('search/page/<int:page>', SearchList.as_view(), name='search'),
]
