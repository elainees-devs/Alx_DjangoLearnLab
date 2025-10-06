from django.urls import path
from .views import RegisterAPIView, CustomObtainAuthToken, ProfileAPIView

urlpatterns=[
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
]