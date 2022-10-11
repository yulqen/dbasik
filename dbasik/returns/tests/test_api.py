from django.test import TestCase
from dbasik.register.models import FinancialQuarter, Project, Tier
from dbasik.returns.models import Return
from dbasik.factories.datamap_factories import ProjectFactory, ProjectTypeFactory, TierFactory


class TestReturnAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tier1 = TierFactory.create()
        cls.project_type1 = ProjectTypeFactory.create()
        cls.project_type1_name = cls.project_type1.name  # we need to know this to test
        cls.project1 = ProjectFactory.create()
        cls.fq1 = FinancialQuarter.objects.create(quarter=2, year=2022)
        cls.return_ = Return.objects.create(
            project=cls.project1, financial_quarter=cls.fq1
        )

    def test_returns_list(self):
        # TODO(mlemon) - continue with this test
        response = self.client.get("/returns/1")
        self.assertEqual(response.status_code, 200)
