import datetime
import unittest

from django.test import TestCase
from django.urls import reverse

from excelparser.helpers.financial_year import Quarter
from excelparser.tests.factories.datamap_factories import (
    ProjectFactory,
    DatamapFactory,
    DatamapLineFactory,
)


class ExcelParserIntegrationTests(TestCase):
    def setUp(self):
        self.financial_quarter = Quarter(2018, 4)
        self.project = ProjectFactory()
        self.datamap = DatamapFactory()
        DatamapLineFactory(key="Project Name", sheet="Test Sheet", cell_ref="B1")
        DatamapLineFactory(key="Total Cost", sheet="Test Sheet", cell_ref="B2")
        DatamapLineFactory(key="SRO", sheet="Test Sheet", cell_ref="B3")
        DatamapLineFactory(key="SRO Retirement Date", sheet="Test Sheet", cell_ref="B4")
        self.populated_template = "/home/lemon/code/python/dbasik-dev/dbasik-dftgovernance/excelparser/tests/populated.xlsm"

    def test_can_get_to_populated_template_upload_page(self):
        response = self.client.get(reverse("excelparser:process_populated"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "excelparser/process_populated_template.html")

    def test_can_post_populated_template_form(self):
        response = self.client.post(
            reverse("excelparser:process_populated"),
            data={
                "datamap": self.datamap,
                "project": self.project,
                "financial_quarter": self.financial_quarter,
                "source_file": self.populated_template,
            },
        )
        self.assertEqual(response.status_code, 200)

    @unittest.skip("Not ready for this yet")
    def test_parsed_spreadsheet_for_single_project(self):
        parsed_spreadsheet = ParseSpreadsheet(
            project=self.project, fq=self.financial_quarter, datamap=self.datamap
        )
        self.assertEqual(parsed_spreadsheet["Project Name"], "Testable Project")
        self.assertEqual(parsed_spreadsheet["Total Cost"], 45.2)
        self.assertEqual(parsed_spreadsheet["SRO"], "John Milton")
        self.assertEqual(
            parsed_spreadsheet["SRO Retirement Date"], datetime.date(2022, 2, 23)
        )
