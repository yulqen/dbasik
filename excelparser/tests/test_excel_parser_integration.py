import unittest

from django.test import TestCase
from django.urls import reverse

from datamap.models import DatamapLine
from excelparser.helpers.parser import ParsedSpreadsheet
from excelparser.helpers.parser import WorkSheetFromDatamap
from excelparser.tests.factories.datamap_factories import DatamapFactory
from excelparser.tests.factories.datamap_factories import DatamapLineFactory
from excelparser.tests.factories.datamap_factories import ProjectFactory
from register.models import FinancialQuarter


class FactoryTests(TestCase):
    """
    These are tests to explore the Factory Boy API.
    """

    def setUp(self):
        self.datamap = DatamapFactory()
        self.project = ProjectFactory()
        self.datamapline = DatamapLineFactory(datamap=self.datamap)

    def test_datamap_factory(self):
        self.assertEqual(self.datamap.name, "Test Datamap from Factory")

    def test_datamapline_factory(self):
        self.assertEqual(self.datamapline.datamap, self.datamap)
        self.assertEqual(self.datamapline.key, "Test key")

    def test_project_factory(self):
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.project_type.name, "Test ProjectType")
        self.assertEqual(self.project.stage.name, "Test Stage")


class ExcelParserIntegrationTests(TestCase):
    def setUp(self):
        self.financial_quarter = FinancialQuarter.objects.create(quarter=4, year=2018)
        self.project = ProjectFactory()
        self.datamap = DatamapFactory()
        DatamapLine.objects.create(datamap=self.datamap, key="Project Name", sheet="Test Sheet 1", cell_ref="B1")
        DatamapLine.objects.create(datamap=self.datamap, key="Total Cost", sheet="Test Sheet 1", cell_ref="B2")
        DatamapLine.objects.create(datamap=self.datamap, key="SRO", sheet="Test Sheet 1", cell_ref="B3")
        DatamapLine.objects.create(
            datamap=self.datamap, key="SRO Retirement Date", sheet="Test Sheet 1", cell_ref="B4"
        )
        self.populated_template = "/home/lemon/code/python/dbasik-dev/dbasik-dftgovernance/excelparser/tests/populated.xlsm"
        self.parsed_spreadsheet = ParsedSpreadsheet(
            template_path=self.populated_template,
            project=self.project,
            fq=self.financial_quarter,
            datamap=self.datamap,
        )

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

    def test_parsed_spreadsheet_for_single_project(self):
        self.assertEqual(
            self.parsed_spreadsheet.sheetnames, ["Test Sheet 1", "Test Sheet 2"]
        )
        self.assertEqual(self.parsed_spreadsheet.project_name, "Test Project")

    def test_getting_sheet_data_using_datamap(self):
        self.parsed_spreadsheet.process()
        test_sheet_1_data = self.parsed_spreadsheet['Test Sheet 1']
        self.assertIsInstance(test_sheet_1_data, WorkSheetFromDatamap)
        self.assertEqual(test_sheet_1_data["Project Name"], "Testable Project")

    @unittest.skip("Not yet implemented")
    def test_strip_colon_from_key(self):
        pass
