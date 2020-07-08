from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "urls"

urlpatterns = [
    path("", views.create, name="create"),
    path("list/", login_required(views.URLListView.as_view()), name="list"),
    path("delete/<pk>/", login_required(views.URLDeleteView.as_view()), name="delete"),
    path("requests/", views.requests, name="requests"),
    path("<slug:slug>/", views.redirect_view),
]
