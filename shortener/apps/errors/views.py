from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def handle_404_view(request: HttpRequest, exception) -> HttpResponse:
    del exception
    return render(request, "404.html", status=404)


def handle_500_view(request: HttpRequest) -> HttpResponse:
    return render(request, "error/500.html", status=500)
