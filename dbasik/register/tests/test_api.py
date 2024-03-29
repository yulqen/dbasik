from dbasik.factories.datamap_factories import (
    ProjectFactory,
    ProjectTypeFactory,
    TierFactory,
)
from dbasik.register.models import FinancialQuarter
from django.test import TestCase


class TestRegisterAPIEndpoints(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tier1 = TierFactory.create()
        cls.project_type1 = ProjectTypeFactory.create()
        cls.project_type1_name = cls.project_type1.name  # we need to know this to test
        cls.project1 = ProjectFactory.create()
        cls.fq1 = FinancialQuarter.objects.create(quarter=2, year=2022)
        cls.fq2 = FinancialQuarter.objects.create(quarter=3, year=2022)

    def test_tier_list(self):
        response = self.client.get("/api/register/tiers")
        self.assertEqual(response.status_code, 200)

    def test_tier(self):
        response = self.client.get("/api/register/tiers/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Tier from Factory")

    def test_project_list(self):
        response = self.client.get("/api/register/projects")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["tier"]["name"], "Test Tier from Factory")

    def test_get_single_project(self):
        response = self.client.get("/api/register/projects/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Project")
        self.assertEqual(response.json()["tier"]["name"], "Test Tier from Factory")

    def test_financial_quarter_list(self):
        response = self.client.get("/api/register/financialquarters")
        self.assertEqual(response.status_code, 200)

    def test_financial_quarter_by_id(self):
        response = self.client.get("/api/register/financialquarters/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["year"], 2022)

    def test_project_types(self):
        response = self.client.get("/api/register/projecttypes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], self.project_type1_name)

    def test_project_type_by_id(self):
        response = self.client.get("/api/register/projecttypes/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], self.project_type1_name)
