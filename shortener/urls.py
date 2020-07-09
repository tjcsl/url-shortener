from django.contrib import admin
from django.urls import include, path

from .apps.errors.views import handle_404_view, handle_500_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("shortener.apps.auth.urls", namespace="auth")),
    path("", include("shortener.apps.urls.urls", namespace="urls")),
    path("oauth/", include("social_django.urls", namespace="social")),
]

handler500 = handle_500_view
