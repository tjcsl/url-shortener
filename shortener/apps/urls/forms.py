from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from nanoid import generate

from .models import URL


class URLForm(forms.ModelForm):

    slug = forms.SlugField(required=False)

    class Meta:
        model = URL
        fields = ("slug", "url", "description")

    def clean(self):
        cleaned_data = self.cleaned_data
        if "slug" not in cleaned_data or not cleaned_data["slug"]:
            cleaned_data["slug"] = generate(size=settings.DEFAULT_SLUG_LENGTH)


class URLApprovalForm(forms.Form):

    qs = URL.objects.filter(approved=False)
    approved = forms.ModelMultipleChoiceField(queryset=qs, required=False)
    denied = forms.ModelMultipleChoiceField(queryset=qs, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        # print(cleaned_data)
        if "approved" in cleaned_data and "denied" in cleaned_data:
            if cleaned_data["approved"].intersection(cleaned_data["denied"]).exists():
                raise ValidationError("Cannot approve and deny the same request!")
