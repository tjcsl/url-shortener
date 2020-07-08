from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.utils.safestring import mark_safe
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render

from .models import URL
from .forms import URLForm, URLApprovalForm

from ..auth.decorators import management_only


def redirect_view(request, slug):
    url = get_object_or_404(URL, slug=slug)
    if url.approved:
        url.visits += 1
        url.save(update_fields=["visits"])
        return redirect(url.url)
    else:
        return render(request, 'urls/not_approved.html')


class URLListView(ListView):
    model = URL
    paginate_by = 10
    ordering = ["-created_at"]
    template_name = "urls/list.html"

    def get_queryset(self):
        return URL.objects.filter(created_by=self.request.user).order_by(*self.ordering)


class URLDeleteView(DeleteView):
    model = URL
    template_name = "urls/delete.html"
    success_url = reverse_lazy("urls:list")
    success_message = "Deleted URL successfully"

    def get_queryset(self):
        return URL.objects.filter(created_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message, extra_tags="success")
        return super().delete(request, *args, **kwargs)


@login_required
def create(request):
    if request.method == "POST":
        pass
    return render(request, "urls/create.html", {"form": URLForm()})


@management_only
def requests(request):
    if request.method == "POST":
        form = URLApprovalForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['approved'].update(approved=True)
            cd['denied'].delete()
            messages.success(request, "Successfully updated requests", extra_tags="success")
        else:
            for errors in form.errors.get_json_data().values():
                for error in errors:
                    messages.error(request, error["message"], extra_tags="danger")
        return redirect("urls:requests")
    page_obj = Paginator(URL.objects.filter(approved=False).order_by('-created_at'), 10).get_page(request.GET.get("page"))
    return render(request, "urls/requests.html", {'page_obj': page_obj, 'form': URLApprovalForm()})

