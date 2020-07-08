from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from .models import URL
from .emails import email_send


@shared_task
def send_action_emails(urls, action, subject):
    for url in urls:
        email_send(
            f'emails/{action}.txt',
            f'emails/{action}.html',
            {
                'slug': url.slug,
                'destination': url
            },
            subject,
            [url.created_by.email]
        )


@shared_task
def delete_old_urls():
    qs = URL.objects.filter(created_at__lt=now() - timedelta(weeks=26))
    send_action_emails(qs, 'deletion', "Short URL Deleted")  # Must be regular function call b/c objects get deleted afterwards
    qs.delete()

