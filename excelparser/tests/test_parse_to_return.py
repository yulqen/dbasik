import unittest

from django.test import TestCase

from datamap.models import DatamapLine
from excelparser.helpers.parser import ParsedSpreadsheet, CellData, CellValueType
from excelparser.tests.factories.datamap_factories import DatamapFactory
from excelparser.tests.factories.datamap_factories import ProjectFactory
from register.models import FinancialQuarter
from returns.models import Return


class TestParseToReturn(TestCase):
    def setUp(self):
        self.financial_quarter = FinancialQuarter.objects.create(quarter=4, year=2018)
        self.project = ProjectFactory()
        self.datamap = DatamapFactory()
        self.return_obj = Return.objects.create(project=self.project, financial_quarter=self.financial_quarter)
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
            return_obj=self.return_obj,
            datamap=self.datamap,
        )

    def test_return_parser(self):
        self.parsed_spreadsheet.process()
        self.parsed_spreadsheet._process_sheet_to_return(self.parsed_spreadsheet["Test Sheet 1"])
        return_item = Return.objects.get(id=self.return_obj.id).returnitem_set.first()
        self.assertEqual(return_item.datamapline.key, "Project Name")
        self.assertEqual(return_item.value_str, "Testable Project")

    def test_celldata_mapper(self):
        self.parsed_spreadsheet.process()
        cell_data = CellData("Key", "Sheet", 1, "B1", CellValueType.INTEGER)
        self.assertEqual(self.parsed_spreadsheet._map_to_keyword_param(cell_data), "value_int")

    @unittest.skip("Not ready to pass")
    def test_parse_to_return_object(self):
        self.parsed_spreadsheet.process()
        return_item = Return.objects.get(id=self.return_obj.id).returnitem_set.first()
        self.assertEqual(return_item.datamapline.key, "Project/Programme Name")
        self.assertEqual(return_item.value_str, "Testable Project")
