from django.test import TestCase
from register.models import FinancialQuarter, Project, Tier
from returns.models import Return


class TestReturnAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tier = Tier.objects.create(name="Tier 1")
        cls.project = Project.objects.create(name="Test Project", tier=cls.tier)
        cls.fq = FinancialQuarter.objects.create(quarter=1, year=2010)
        cls.return_ = Return.objects.create(
            project=cls.project, financial_quarter=cls.fq
        )

    def test_returns_list(self):
        response = self.client.get("/returns/1")
        self.assertEqual(response.status_code, 200)
