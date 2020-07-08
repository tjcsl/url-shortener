from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def login(request: HttpRequest) -> HttpResponse:
    return render(request, "auth/login.html")


def error(request: HttpRequest) -> HttpResponse:
    return render(request, "auth/error.html")
