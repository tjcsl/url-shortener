from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView

from ..auth.decorators import management_only
from .forms import URLApprovalForm, URLForm
from .models import URL
from .tasks import send_action_emails


def redirect_view(request: HttpRequest, slug: str) -> HttpResponse:
    url = get_object_or_404(URL, slug=slug)
    if url.approved:
        url.visits += 1
        url.save(update_fields=["visits"])
        return redirect(url.url)
    else:
        return render(request, "urls/not_approved.html")


class URLListView(ListView):
    model = URL
    paginate_by = 10
    ordering = ["-created_at"]
    template_name = "urls/list.html"

    def get_queryset(self) -> "models.query.QuerySet[URL]":
        return URL.objects.filter(created_by=self.request.user).order_by(*self.ordering)


class URLDeleteView(DeleteView):
    model = URL
    template_name = "urls/delete.html"
    success_url = reverse_lazy("urls:list")
    success_message = "Deleted URL successfully"

    def get_queryset(self) -> "models.query.QuerySet[URL]":
        return URL.objects.filter(created_by=self.request.user)

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        messages.success(request, self.success_message, extra_tags="success")
        return super().delete(request, *args, **kwargs)


@login_required
def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            url.created_by = request.user
            host = f"{request.is_secure() and 'https' or 'http'}://{request.get_host()}/{url.slug}"
            if request.user.has_management_permission:
                messages.success(
                    request,
                    mark_safe(f'Successfully created short URL at <a href="{url.url}">{host}</a>'),
                )
                url.approved = True
            else:
                messages.success(
                    request, mark_safe(f"Successfully requested URL shortening, awaiting approval.")
                )
                messages.success(
                    request,
                    mark_safe(
                        f'If approved short URL <a href="{host}">{host}</a> will redirect to destination'
                    ),
                )
                url.approved = False
            url.save()
        else:
            for errors in form.errors.get_json_data().values():
                for error in errors:
                    messages.error(request, error["message"], extra_tags="danger")
    return render(request, "urls/create.html", {"form": URLForm()})


@management_only
def requests(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = URLApprovalForm(data=request.POST)
        host = f"{request.is_secure() and 'https' or 'http'}://{request.get_host()}"
        if form.is_valid():
            cd = form.cleaned_data
            send_action_emails.delay(
                [x.id for x in cd["approved"]],
                "approved",
                "Short URL Request Approved",
                host,
            )
            send_action_emails.delay(
                [x.id for x in cd["denied"]],
                "denied",
                "Short URL Request Denied",
                host,
            )
            cd["approved"].update(approved=True)
            cd["denied"].delete()
            messages.success(request, "Successfully updated requests", extra_tags="success")
        else:
            for errors in form.errors.get_json_data().values():
                for error in errors:
                    messages.error(request, error["message"], extra_tags="danger")
    page_obj = Paginator(URL.objects.filter(approved=False).order_by("-created_at"), 10).get_page(
        request.GET.get("page")
    )
    return render(request, "urls/requests.html", {"page_obj": page_obj, "form": URLApprovalForm()})


def help(request: HttpRequest) -> HttpResponse:
    return render(request, "urls/help.html")
