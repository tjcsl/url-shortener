from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404

from .models import URL
from .forms import URLForm


class URLRedirectView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(URL, kwargs['slug'])
        return super().get_redirect_url(url=url.url)


class CreateView(FormView):
    form_class = URLForm
    template_name = 'urls/create.html'
    success_url = reverse_lazy("urls:create")

    def form_valid(self, form):
        print(form)
        host = f"{self.request.is_secure() and 'https' or 'http'}://{self.request.get_host()}/{form.cleaned_data['slug']}"
        messages.success(self.request, f"Successfully created short URL: {host}", extra_tags="success")
        return super().form_valid(form)

    def form_invalid(self, form):
        for errors in form.errors.get_json_data().values():
            for error in errors:
                messages.error(self.request, error["message"], extra_tags="danger")

        return super().form_invalid(form)
