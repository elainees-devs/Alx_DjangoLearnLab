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
path('post/new/', views.PostCreateView.as_view(), name='post_create'), #Create new post
path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), #View single post
path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_edit'), #Edit post
path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete') #Delete post
]