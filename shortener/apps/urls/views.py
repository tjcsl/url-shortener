from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect

from .models import URL
from .forms import URLForm


def redirect_view(request, slug):
    url = get_object_or_404(URL, slug=slug)
    return redirect(url.url)


class CreateView(FormView):
    form_class = URLForm
    template_name = 'urls/create.html'
    success_url = reverse_lazy("urls:create")

    def form_valid(self, form):
        url = form.save(commit=False)
        url.created_by = self.request.user
        url.save()
        host = f"{self.request.is_secure() and 'https' or 'http'}://{self.request.get_host()}/{url.slug}"
        messages.success(self.request, f"Successfully created short URL: {host}", extra_tags="success")
        return super().form_valid(form)

    def form_invalid(self, form):
        for errors in form.errors.get_json_data().values():
            for error in errors:
                messages.error(self.request, error["message"], extra_tags="danger")

        return super().form_invalid(form)
