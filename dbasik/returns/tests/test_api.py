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
            name="Test DM", active=True, slug="test-dm-test-tier-1"
        )
        cls.dml1 = DatamapLine.objects.create(
            datamap=cls.dm1,
            key="Test Key",
            data_type="TEXT",
            required=True,
            sheet="Test Sheet",
            cell_ref="A1",
        )
        cls.dml2 = DatamapLine.objects.create(
            datamap=cls.dm1,
            key="Test Key 2",
            data_type="NUMBER",
            required=True,
            sheet="Test Sheet",
            cell_ref="A2",
        )
        cls.ri1 = ReturnItem.objects.create(
            parent=cls.return_, datamapline=cls.dml1, value_str="Value String"
        )
        cls.ri1 = ReturnItem.objects.create(
            parent=cls.return_, datamapline=cls.dml2, value_int=1
        )

    def test_returns(self):
        """List of returns."""
        response = self.client.get("/api/returns/returns")
        self.assertEqual(response.status_code, 200)

    def test_return(self):
        """Single return by ID."""
        response = self.client.get("/api/returns/returns/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project"]["name"], "Test Project")
        self.assertEqual(response.json()["financial_quarter"]["year"], 2022)

    def test_returns_for_quarter(self):
        """Grab all the returns for a FQ."""
        response = self.client.get("/api/returns/returns-for-quarter/1")
        self.assertEqual(response.status_code, 200)
        # TODO: fix types
        self.assertEqual(
            response.json()[0]["parent"]["project"]["name"], self.project1.name
        )
