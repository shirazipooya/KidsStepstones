from django.urls import path
from .views import (
    HomeView,
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    Profile,
)

app_name = "dashboard"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("posts/create", PostCreateView.as_view(), name="post-create"),
    path("posts/update/<int:pk>", PostUpdateView.as_view(), name="post-update"),
    path("posts/delete/<int:pk>", PostDeleteView.as_view(), name="post-delete"),
    path("profile/", Profile.as_view(), name="profile"),
]