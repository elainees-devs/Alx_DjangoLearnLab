from django.urls import path
from .views import RegisterAPIView, CustomObtainAuthToken, ProfileAPIView
from . import views

urlpatterns=[
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('follow/<int:user_id>/', views.FollowUserAPIView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', views.UnfollowUserAPIView.as_view(), name='unfollow-user'),
    path('users/<int:user_id>/followers/', views.UserFollowersAPIView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', views.UserFollowingAPIView.as_view(), name='user-following'),
]