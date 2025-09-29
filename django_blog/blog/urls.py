from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)


urlpatterns = [
path('register/', views.register, name='register'),
path('login/', views.CustomLoginView.as_view(), name='login'),
path('logout/', views.CustomLogoutView.as_view(), name='logout'),
path('profile/', views.profile_view, name='profile'),

# Blog Post CRUD
path('posts/', views.PostListView.as_view(), name='post_list'), #List all posts
path('posts/new/', views.PostCreateView.as_view(), name='post_create'), #Create new post
path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), #View single post
path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'), #Edit post
path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete') #Delete post
]