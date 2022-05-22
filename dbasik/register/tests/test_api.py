from django.test import Client, TestCase
from register.models import Tier


class TestRegisterAPIEndpoints(TestCase):
    def setUp(self):
        self.client = Client()
        self.tier1 = Tier.objects.create(name="Tier 1")
        self.tier1.save()

    def test_tier_list(self):
        response = self.client.get("/api/tiers/")
        self.assertEqual(response.status_code, 200)

    def test_tier(self):
        response = self.client.get("/api/tiers/1/")
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()["name"], "Tier 1")
