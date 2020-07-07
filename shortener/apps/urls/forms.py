from django import forms
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from nanoid import generate

from .models import URL


class URLForm(forms.ModelForm):

    slug = forms.SlugField(required=False)

    class Meta:
        model = URL
        fields = ['slug', 'url']

    def full_clean(self):
        try:
            super().full_clean()
        except IntegrityError:
            raise ValidationError("custom slug already in use")

    def clean(self):
        cd = self.cleaned_data
        if 'slug' not in cd:
            cd['slug'] = generate(size=15)
