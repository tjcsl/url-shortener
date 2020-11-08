from django.urls import reverse

from ...test.shortener_test import ShortnerTestCase


class AuthTest(ShortnerTestCase):
    def test_login_view(self):
        response = self.client.get(reverse("auth:login"), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "auth/login.html")

    def test_error_view(self):
        response = self.client.get(reverse("auth:error"), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "auth/error.html")

    def test_logout_view(self):
        self.login(make_teacher=False, make_student=True)
        response = self.client.get(reverse("auth:logout"), follow=True)
        self.assertEqual(200, response.status_code)

        # To check if we've been logged out, try to load a page that requires login
        response = self.client.get(reverse("urls:create"))
        self.assertEqual(302, response.status_code)  # redirect to login

    def test_user_model(self):
        user = self.login(username="2020awilliam", make_teacher=False, make_student=True)
        self.assertEqual("2020awilliam", user.short_name)
        self.assertFalse(user.has_management_permission)
        self.assertEqual("2020awilliam", str(user))

        user = self.login(
            username="2020awilliam", make_teacher=False, make_student=True, make_superuser=True
        )
        self.assertEqual("2020awilliam", user.short_name)
        self.assertTrue(user.has_management_permission)
        self.assertEqual("2020awilliam", str(user))

        user = self.login(
            username="awilliam", make_teacher=True, make_student=False, make_superuser=False
        )
        self.assertEqual("awilliam", user.short_name)
        self.assertTrue(user.has_management_permission)
        self.assertEqual("awilliam", str(user))
