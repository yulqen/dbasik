import datetime

from django.test import TestCase
from django.urls import reverse

from datamap.models import DatamapLine
from excelparser.helpers.parser import CellData
from excelparser.helpers.parser import CellValueType
from excelparser.helpers.parser import MissingSheetError
from excelparser.helpers.parser import ParsedSpreadsheet
from excelparser.helpers.parser import WorkSheetFromDatamap
from excelparser.helpers.parser import _detect_cell_type
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
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Project Name",
            sheet="Test Sheet 1",
            cell_ref="B1",
        )
        DatamapLine.objects.create(
            datamap=self.datamap, key="Total Cost", sheet="Test Sheet 1", cell_ref="B2"
        )
        DatamapLine.objects.create(
            datamap=self.datamap, key="SRO", sheet="Test Sheet 1", cell_ref="B3"
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="SRO Retirement Date",
            sheet="Test Sheet 1",
            cell_ref="B4",
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Janitor's Favourite Colour",
            sheet="Test Sheet 2",
            cell_ref="B1",
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
        test_sheet_1_data = self.parsed_spreadsheet["Test Sheet 1"]

        self.assertIsInstance(test_sheet_1_data, WorkSheetFromDatamap)
        self.assertIsInstance(test_sheet_1_data["Project Name"], CellData)

        self.assertEqual(test_sheet_1_data["Project Name"].value, "Testable Project")
        self.assertEqual(test_sheet_1_data["Project Name"].sheet, "Test Sheet 1")
        self.assertEqual(test_sheet_1_data["Project Name"].type, CellValueType.STRING)
        self.assertEqual(test_sheet_1_data["Project Name"].source_cell, "B1")
        self.assertEqual(test_sheet_1_data["Project Name"].key, "Project Name")

        self.assertEqual(test_sheet_1_data["Total Cost"].value, 45.2)
        self.assertEqual(test_sheet_1_data["Total Cost"].sheet, "Test Sheet 1")
        self.assertEqual(test_sheet_1_data["Total Cost"].type, CellValueType.FLOAT)
        self.assertEqual(test_sheet_1_data["Total Cost"].source_cell, "B2")
        self.assertEqual(test_sheet_1_data["Total Cost"].key, "Total Cost")

        self.assertEqual(test_sheet_1_data["SRO"].value, "John Milton")
        self.assertEqual(test_sheet_1_data["SRO"].sheet, "Test Sheet 1")
        self.assertEqual(test_sheet_1_data["SRO"].type, CellValueType.STRING)
        self.assertEqual(test_sheet_1_data["SRO"].source_cell, "B3")
        self.assertEqual(test_sheet_1_data["SRO"].key, "SRO")

        self.assertEqual(
            test_sheet_1_data["SRO Retirement Date"].value,
            datetime.datetime(2022, 2, 23),
        )
        self.assertEqual(test_sheet_1_data["SRO Retirement Date"].sheet, "Test Sheet 1")
        self.assertEqual(
            test_sheet_1_data["SRO Retirement Date"].type, CellValueType.DATETIME
        )
        self.assertEqual(test_sheet_1_data["SRO Retirement Date"].source_cell, "B4")
        self.assertEqual(
            test_sheet_1_data["SRO Retirement Date"].key, "SRO Retirement Date"
        )

    def test_getting_separate_sheet_data(self):
        self.parsed_spreadsheet.process()
        test_sheet_2_data = self.parsed_spreadsheet["Test Sheet 2"]

        self.assertIsInstance(test_sheet_2_data, WorkSheetFromDatamap)
        self.assertIsInstance(test_sheet_2_data["Janitor's Favourite Colour"], CellData)

        self.assertEqual(
            test_sheet_2_data["Janitor's Favourite Colour"].value, "Purple"
        )
        self.assertEqual(
            test_sheet_2_data["Janitor's Favourite Colour"].sheet, "Test Sheet 2"
        )
        self.assertEqual(
            test_sheet_2_data["Janitor's Favourite Colour"].type, CellValueType.STRING
        )
        self.assertEqual(
            test_sheet_2_data["Janitor's Favourite Colour"].source_cell, "B1"
        )
        self.assertEqual(
            test_sheet_2_data["Janitor's Favourite Colour"].key,
            "Janitor's Favourite Colour",
        )

    def test_exception_raised_when_dml_sheet_and_actual_sheet_dont_match(self):

        dodgy_datamap = DatamapFactory()

        DatamapLine.objects.create(
            datamap=dodgy_datamap,
            key="Dodgy Line",
            sheet="Test Sheet NONEXISTENT",
            cell_ref="B1",
        )

        with self.assertRaises(MissingSheetError):
            ParsedSpreadsheet(
                template_path=self.populated_template,
                project=self.project,
                fq=self.financial_quarter,
                datamap=dodgy_datamap,
            )

        with self.assertRaisesMessage(
            MissingSheetError,
            "There is a worksheet in the spreadsheet not in the Datamap - Test Sheet NONEXISTENT",
        ):
            ParsedSpreadsheet(
                template_path=self.populated_template,
                project=self.project,
                fq=self.financial_quarter,
                datamap=dodgy_datamap,
            )

    def test_map_type_to_cellvaluetype_enum(self):
        self.assertEqual(_detect_cell_type(1), CellValueType.INTEGER)

    def test_type_detect_exception(self):
        self.assertRaises(ValueError, _detect_cell_type, ["test"])
        self.assertRaisesMessage(
            ValueError, "Cannot detect applicable type", _detect_cell_type, []
        )

    def test_parsed_spreadsheet_metadata(self):
        self.parsed_spreadsheet.process()
        self.assertEqual(self.parsed_spreadsheet.filename, "populated.xlsm")
        self.assertEqual(self.parsed_spreadsheet.project_name, "Test Project")

    def test_exception_if_non_str_index_used(self):
        self.parsed_spreadsheet.process()
        with self.assertRaises(TypeError):
            tmp = self.parsed_spreadsheet[1]
        with self.assertRaises(TypeError):
            tmp = self.parsed_spreadsheet[[1]]

    def test_non_attribute_access(self):
        self.parsed_spreadsheet.process()
        with self.assertRaisesMessage(
            MissingSheetError,
            "There is no sheet in the spreadsheet with title MISSING " "SHEET.",
        ):
            tmp = self.parsed_spreadsheet["MISSING SHEET"]
