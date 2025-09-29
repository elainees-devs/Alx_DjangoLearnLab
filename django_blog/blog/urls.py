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
path('posts/', PostListView.as_view(), name='post_list'),
path('posts/new/', PostCreateView.as_view(), name='post_create'),
path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]