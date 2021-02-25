from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from ...test.shortener_test import ShortnerTestCase
from .models import URL
from .tasks import delete_old_urls


class URLTests(ShortnerTestCase):
    def test_redirect_view(self):
        user = self.login(make_teacher=True)
        URL.objects.create(
            slug="sysadmins", url="https://sysadmins.tjhsst.edu", created_by=user, approved=True
        )

        response = self.client.get("/sysadmins/", follow=False)
        self.assertRedirects(
            response, "https://sysadmins.tjhsst.edu", fetch_redirect_response=False
        )

        URL.objects.create(
            slug="example", url="https://www.example.com", created_by=user, approved=False
        )

        response = self.client.get("/example/", follow=False)
        self.assertTemplateUsed(response, "urls/not_approved.html")

    def test_list_view(self):
        user = self.login(make_teacher=True)
        response = self.client.get(reverse("urls:list"))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.context["page_obj"]))

        URL.objects.create(
            slug="sysadmins", url="https://sysadmins.tjhsst.edu", created_by=user, approved=True
        )
        URL.objects.create(
            slug="example", url="https://www.example.com", created_by=user, approved=False
        )

        response = self.client.get(reverse("urls:list"))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context["page_obj"]))

    def test_delete_view(self):
        user = self.login(make_teacher=True)
        url = URL.objects.create(
            slug="sysadmins", url="https://sysadmins.tjhsst.edu", created_by=user, approved=True
        )

        response = self.client.get(reverse("urls:delete", kwargs={"pk": url.id}), follow=True)
        self.assertEqual(200, response.status_code)

        response = self.client.post(reverse("urls:delete", kwargs={"pk": url.id}), follow=True)
        self.assertEqual(200, response.status_code)

        self.assertEqual(0, len(URL.objects.filter(slug="sysadmins")))

    def test_create_view(self):
        user = self.login(make_teacher=True)

        response = self.client.get(reverse("urls:create"), follow=True)
        self.assertEqual(200, response.status_code)

        response = self.client.post(
            reverse("urls:create"),
            follow=True,
            data={
                "slug": "sysadmins",
                "url": "https://sysadmins.tjhsst.edu",
                "description": "Test",
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            1, len(URL.objects.filter(slug="sysadmins", created_by=user, approved=True))
        )

        user = self.login(username="2020awilliam", make_student=True)

        response = self.client.post(
            reverse("urls:create"),
            follow=True,
            data={
                "slug": "test",
                "url": "https://example.com",
                "description": "Test",
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(URL.objects.filter(slug="test", created_by=user, approved=False)))

        # Test an invalid entry.
        response = self.client.post(
            reverse("urls:create"),
            follow=True,
            data={
                "slug": "test1",
                "url": "https://examplecom",
                "description": "Test",
            },
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(URL.objects.filter(slug="test1")))

        self.assertGreaterEqual(1, len(list(response.context["messages"])))

        # Test creating a URL without specifying a slug.
        response = self.client.post(
            reverse("urls:create"),
            follow=True,
            data={
                "url": "https://www.example.com",
                "description": "Test",
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            1,
            len(URL.objects.filter(url="https://www.example.com", created_by=user, approved=False)),
        )
        self.assertEqual(
            settings.DEFAULT_SLUG_LENGTH,
            len(
                URL.objects.get(url="https://www.example.com", created_by=user, approved=False).slug
            ),
        )

    def test_requests_view(self):
        student = self.login(username="2020awilliam", make_student=True)
        self.login(make_teacher=True)

        response = self.client.get(reverse("urls:requests"), follow=True)
        self.assertEqual(200, response.status_code)

        url = URL.objects.create(
            slug="sysadmins", url="https://sysadmins.tjhsst.edu", created_by=student, approved=False
        )
        url2 = URL.objects.create(
            slug="sysadmins2",
            url="https://sysadmins.tjhsst.edu",
            created_by=student,
            approved=False,
        )

        # Test an invalid entry.
        response = self.client.post(
            reverse("urls:requests"), follow=True, data={"approved": [url.id], "denied": [url.id]}
        )
        self.assertEqual(200, response.status_code)
        self.assertIn(
            "Cannot approve and deny the same request!",
            list(map(str, list(response.context["messages"]))),
        )

        response = self.client.get(reverse("urls:requests"), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context["page_obj"]))

        response = self.client.post(
            reverse("urls:requests"), follow=True, data={"approved": [url.id, url2.id]}
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(URL.objects.filter(slug="sysadmins", approved=True)))
        self.assertEqual(1, len(URL.objects.filter(slug="sysadmins2", approved=True)))

    def test_help_view(self):
        self.login(make_teacher=True)
        response = self.client.get(reverse("urls:help"), follow=True)
        self.assertTemplateUsed(response, "urls/help.html")

    def test_delete_old_urls(self):
        student = self.login(username="2020awilliam", make_student=True)
        url = URL.objects.create(
            slug="sysadmins", url="https://sysadmins.tjhsst.edu", created_by=student, approved=False
        )
        url2 = URL.objects.create(
            slug="sysadmins2",
            url="https://sysadmins.tjhsst.edu",
            created_by=student,
            approved=False,
            created_at=timezone.localtime() - timezone.timedelta(weeks=52),
        )

        delete_old_urls()

        self.assertEqual(1, URL.objects.filter(id=url.id).count())
        self.assertEqual(0, URL.objects.filter(id=url2.id).count())
