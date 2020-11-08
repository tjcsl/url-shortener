from django.test import RequestFactory

from ...test.shortener_test import ShortnerTestCase
from .views import handle_500_view


class ErrorsTestCase(ShortnerTestCase):
    def test_handle_500_view(self):
        factory = RequestFactory()
        request = factory.get("/")
        response = handle_500_view(request)

        self.assertEqual(500, response.status_code)
