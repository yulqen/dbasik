import pathlib
import unittest

from django.test import TestCase
from django.urls import reverse

from datamap.models import DatamapLine
from factories.datamap_factories import DatamapFactory
from factories.datamap_factories import ProjectFactory
from register.models import FinancialQuarter
from returns.models import Return


class TestExcelParserViews(TestCase):
    def setUp(self):
        self.populated_template = (
            pathlib.Path(__file__).parent.absolute() / "populated.xlsm"
        )
        self.project = ProjectFactory()
        self.datamap = DatamapFactory()
        self.dml1 = DatamapLine(datamap=self.datamap)
        self.fq = FinancialQuarter.objects.create(quarter=1, year=2010)
        self.return_obj = Return.objects.create(
            project=self.project, financial_quarter=self.fq
        )

    @unittest.skip("Unknown reason at this point - TBC")
    def test_upload_single_populated_has_correct_header(self):
        response = self.client.get(
            reverse("excelparser:process_populated", args=[self.return_obj.id])
        )
        self.assertTrue(response.status_code, 200)
        self.assertContains(
            response, f"<legend>Process a populated template for Test Project</legend>"
        )

    @unittest.skip("Unknown reason at this point - TBC")
    def test_view_receives_uploaded_file(self):
        response = self.client.post(
            f"/excelparser/process-populated/{self.return_obj.id}/",
            {
                "return_obj": self.return_obj,
                "datamap": self.datamap,
                "source_file": self.populated_template,
            },
        )
        self.assertEqual(response.status_code, 200)
