from datetime import timedelta

from celery import shared_task
from django.db import models
from django.utils.timezone import now

from .emails import email_send
from .models import URL


@shared_task
def send_action_emails(urls: "models.query.QuerySet[URL]", action: str, subject: str) -> None:
    for url in urls:
        email_send(
            f"emails/{action}.txt",
            f"emails/{action}.html",
            {"slug": url.slug, "destination": url},
            subject,
            [url.created_by.email],
        )


@shared_task
def delete_old_urls() -> None:
    qs = URL.objects.filter(created_at__lt=now() - timedelta(weeks=26))
    send_action_emails(
        qs, "deletion", "Short URL Deleted"
    )  # Must be regular function call b/c objects get deleted afterwards
    qs.delete()
