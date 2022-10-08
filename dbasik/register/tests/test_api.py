from dbasik.register.models import Tier
from django.test import TestCase


class TestRegisterAPIEndpoints(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tier1 = Tier.objects.create(name="Tier 1")

    def test_tier_list(self):
        response = self.client.get("/api/register/tiers")
        self.assertEqual(response.status_code, 200)

    def test_tier(self):
        response = self.client.get("/api/register/tiers/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Tier 1")

    # TODO(matt) work on this next it's failing
    def test_project_list(self):
        response = self.client.get("/api/projects/")
        self.assertEqual(response.status_code, 200)
