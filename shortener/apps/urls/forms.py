from nanoid import generate

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import URL


class URLForm(forms.ModelForm):

    slug = forms.SlugField(required=False)

    class Meta:
        model = URL
        fields = ("slug", "url", "description")

    def clean(self):
        cd = self.cleaned_data
        if "slug" not in cd or not cd["slug"]:
            cd["slug"] = generate(size=settings.DEFAULT_SLUG_LENGTH)


class URLApprovalForm(forms.Form):

    qs = URL.objects.filter(approved=False)
    approved = forms.ModelMultipleChoiceField(queryset=qs, required=False)
    denied = forms.ModelMultipleChoiceField(queryset=qs, required=False)

    def __init__(self, *args, **kwargs):
        super(URLApprovalForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        print(cd)
        if "approved" in cd and "denied" in cd:
            if cd["approved"].intersection(cd["denied"]).exists():
                raise ValidationError("Cannot approve and deny the same request!")
