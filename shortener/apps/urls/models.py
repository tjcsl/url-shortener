from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now


class URL(models.Model):

    slug = models.SlugField()
    url = models.URLField()

    visits = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="urls")

    approved = models.BooleanField(default=False)
    description = models.CharField(max_length=2000, default="")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["slug"], name="unique_slug")]

    def clean(self):
        self.validate_unique()

    def __str__(self):
        return f"tiny.tjhsst.edu/{self.slug} -> {self.url}"

    def __repr__(self):
        return f"<URL {self.id}: {self.slug} {self.url}"
