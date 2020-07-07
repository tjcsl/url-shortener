from django import forms

from nanoid import generate

from .models import URL


class URLForm(forms.ModelForm):

    slug = forms.SlugField(required=False)

    class Meta:
        model = URL
        fields = ('slug', 'url')

    def clean(self):
        cd = self.cleaned_data
        if 'slug' not in cd or not cd['slug']:
            cd['slug'] = generate(size=15)
