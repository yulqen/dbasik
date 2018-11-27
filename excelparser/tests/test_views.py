from django.test import TestCase

from datamap.models import DatamapLine
from excelparser.tests.factories.datamap_factories import DatamapFactory
from excelparser.tests.factories.datamap_factories import ProjectFactory
from register.models import FinancialQuarter
from returns.models import Return


class TestExcelParserViews(TestCase):
    def setUp(self):
        self.populated_template = "/home/lemon/code/python/dbasik-dev/dbasik-dftgovernance/excelparser/tests/populated.xlsm"
        self.project = ProjectFactory()
        self.datamap = DatamapFactory()
        self.dml1 = DatamapLine(datamap=self.datamap)
        self.fq = FinancialQuarter.objects.create(quarter=1, year=2010)
        self.return_obj = Return.objects.create(
            project=self.project, financial_quarter=self.fq
        )

    def test_view_receives_uploaded_file(self):
        response = self.client.post(
            f"/excelparser/process-populated/{self.return_obj.id}/",
            {
                "return_obj": self.return_obj,
                "financial_quarter": self.fq,
                "datamap": self.datamap,
                "source_file": self.populated_template,
            },
        )
        self.assertEqual(response.status_code, 200)
