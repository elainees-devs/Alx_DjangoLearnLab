from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    # HTML template view
    path('', views.notification_list, name='notification_list'),

    # API view
    # path('api/', views.NotificationListView.as_view(), name='notification_list_api'),
]
