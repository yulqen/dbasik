from django.test import TestCase
from django.urls import reverse


class ReturnsViewsTests(TestCase):
    def test_list_of_financial_quarters(self):
        response = self.client.get(reverse("returns:financial_quarters"))
        self.assertTrue(response.status_code, 200)
