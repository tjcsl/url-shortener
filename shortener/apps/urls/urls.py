from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "urls"

urlpatterns = [
    path("", login_required(views.CreateView.as_view()), name="create"),
    path("<slug:slug>/", views.redirect_view),
]
