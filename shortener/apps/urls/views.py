from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView, DeleteView

from .models import URL
from .forms import URLForm


def redirect_view(request, slug):
    url = get_object_or_404(URL, slug=slug)
    url.visits += 1
    url.save(update_fields=["visits"])
    return redirect(url.url)


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


class CreateView(FormView):
    form_class = URLForm
    template_name = 'urls/create.html'
    success_url = reverse_lazy("urls:create")

    def form_valid(self, form):
        url = form.save(commit=False)
        url.created_by = self.request.user
        url.save()
        host = f"{self.request.is_secure() and 'https' or 'http'}://{self.request.get_host()}/{url.slug}"
        messages.success(self.request, mark_safe(f"Successfully created short URL: <a href=\"{host}\">{host}</a>"), extra_tags="success")
        return super().form_valid(form)

    def form_invalid(self, form):
        for errors in form.errors.get_json_data().values():
            for error in errors:
                messages.error(self.request, error["message"], extra_tags="danger")

        return super().form_invalid(form)
