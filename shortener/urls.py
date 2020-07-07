from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("shortener.apps.auth.urls", namespace="auth")),
    path("", include("shortener.apps.urls.urls", namespace="urls")),
    path("oauth/", include("social_django.urls", namespace="social")),
]
