from dbasik.datamap.models import Datamap, DatamapLine
from dbasik.factories.datamap_factories import (
    ProjectFactory,
    ProjectTypeFactory,
    TierFactory,
)
from dbasik.register.models import FinancialQuarter
from dbasik.returns.models import Return, ReturnItem
from django.test import TestCase


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
        cls.dm1 = Datamap.objects.create(
            name="Test DM", tier=cls.tier1, active=True, slug="test-dm-test-tier-1"
        )
        cls.dml1 = DatamapLine.objects.create(
            datamap=cls.dm1,
            key="Test Key",
            data_type="TEXT",
            required=True,
            sheet="Test Sheet",
            cell_ref="A1",
        )
        cls.ri1 = ReturnItem.objects.create(
            parent=cls.return_, datamapline=cls.dml1, value_str="Value String"
        )

    def test_returns(self):
        """List of returns."""
        response = self.client.get("/api/returns/returns")
        self.assertEqual(response.status_code, 200)
