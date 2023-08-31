from django.urls import path
from .views import home, PostListView, PostCreateView

app_name = "dashboard"
urlpatterns = [
    path("", home, name="home"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("posts/create", PostCreateView.as_view(), name="post-create"),
]