from dbasik.factories.datamap_factories import (
    ProjectFactory,
    ProjectTypeFactory,
    TierFactory,
)
from django.test import TestCase


class TestRegisterAPIEndpoints(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tier1 = TierFactory.create()
        cls.project_type1 = ProjectTypeFactory.create()
        cls.project1 = ProjectFactory.create()

    def test_tier_list(self):
        response = self.client.get("/api/register/tiers")
        self.assertEqual(response.status_code, 200)

    def test_tier(self):
        response = self.client.get("/api/register/tiers/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Tier 1")

    def test_project_list(self):
        response = self.client.get("/api/register/projects")
        self.assertEqual(response.status_code, 200)

    def test_get_single_project(self):
        response = self.client.get("/api/register/projects/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Project")
