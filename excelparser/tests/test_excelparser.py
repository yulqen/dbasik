import datetime
import unittest

from django.test import TestCase

from excelparser.helpers import Quarter, FinancialYear
from excelparser.tests.factories.datamap_factories import ProjectFactory
from .factories.datamap_factories import DatamapFactory, DatamapLineFactory


class TestFinancialYear(TestCase):

    def test_financial_year_creation(self):
        fy = FinancialYear(2010)
        self.assertEqual(fy.year, 2010)
        self.assertEqual(fy.end_date, datetime.date(2011, 3, 31))

    def test_financial_year_objects_are_equal(self):
        fy1 = FinancialYear(2010)
        fy2 = FinancialYear(2010)
        self.assertEqual(fy1, fy2)

    @unittest.skip("Cannot pass yet")
    def test_financial_quarter_creation(self):
        fy = FinancialYear(2010)
        q = Quarter(1, 2010)
        self.assertEqual(q.fy, fy)



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


    def test_parsed_spreadsheet_for_single_project(self):
        parsed_spreadsheet = ParseSpreadsheet(project=self.project, fq=self.financial_quarter, datamap=self.datamap)
        self.assertEqual(parsed_spreadsheet['Project Name'], "Testable Project")
        self.assertEqual(parsed_spreadsheet['Total Cost'], 45.2)
        self.assertEqual(parsed_spreadsheet['SRO'], "John Milton")
        self.assertEqual(parsed_spreadsheet['SRO Retirement Date'], datetime.date(2022, 2, 23))
