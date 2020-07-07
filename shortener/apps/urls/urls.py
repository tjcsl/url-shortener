from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "urls"

urlpatterns = [
    path("<slug:slug>/", views.URLRedirectView.as_view()),
    path("", login_required(views.CreateView.as_view()), name="create"),
]
