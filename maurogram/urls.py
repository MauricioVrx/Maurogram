"""Maurogram URLs module."""

# Django
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import logout
from django.urls import path, include

from maurogram import views as local_views
from users import views as users_views


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include(('posts.urls','posts'),namespace='posts')),
    path('users/', include(('users.urls','users'),namespace='users')),
    # path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)