from typing import List

from openpyxl import load_workbook
from openpyxl.worksheet import Worksheet

from datamap.models import Datamap
from register.models import FinancialQuarter
from register.models import Project


class ParsedSpreadsheet:
    def __init__(
        self,
        template_path: str,
        project: Project,
        fq: FinancialQuarter,
        datamap: Datamap,
    ):
        self.template_path = template_path
        self._project = project
        self.fq = fq
        self.datamap = datamap
        self.sheet_data: List[Worksheet] = []

        self._get_sheets()

    def _process_sheets(self):
        wb = load_workbook(self.template_path)
        for ws in self.sheets:
            self.sheet_data.append(wb[ws])

    def process(self):
        self._process_sheets()

    @property
    def project_name(self) -> str:
        return self._project.name

    def _get_sheets(self) -> None:
        wb = load_workbook(self.template_path)
        self.sheets = wb.sheetnames


def convert_openpyxl_worksheet(test_sheet_1_data: Worksheet, datamap: Datamap):
    return WorkSheetFromDatamap(test_sheet_1_data, datamap)


class WorkSheetFromDatamap:
    def __init__(self, openpyxl_worksheet: Worksheet, datamap: Datamap):
        self._data = {}
        self.openpyxl_worksheet = openpyxl_worksheet
        self.datamap = datamap
        self._convert()

    def __getitem__(self, item):
        return self._data[item]

    def _convert(self):
        for dml in self.datamap.datamapline_set.all():
            key = dml.key
            value = self.openpyxl_worksheet[dml.cell_ref].value
            self._data[key] = value
