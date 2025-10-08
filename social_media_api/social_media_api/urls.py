from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to the Social Media API")


urlpatterns = [
path('', home),  # root path
path('admin/', admin.site.urls),
path('api/accounts/', include('accounts.urls')),
path('api/posts/', include('posts.urls')),
path('api/', include('notifications.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)