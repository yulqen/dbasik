from typing import List

from openpyxl import load_workbook
from openpyxl import Workbook as OpenpyxlWorkbook
from openpyxl.worksheet import Worksheet as OpenpyxlWorksheet

from datamap.models import Datamap
from register.models import FinancialQuarter
from register.models import Project

SheetData = List[OpenpyxlWorksheet]


class ParsedSpreadsheet:
    def __init__(
        self,
        template_path: str,
        project: Project,
        fq: FinancialQuarter,
        datamap: Datamap,
    ) -> None:
        self.template_path = template_path
        self._project = project
        self.fq = fq
        self.datamap = datamap
        self.sheet_data: SheetData = []
        self.sheetnames: List[str]

        self._get_sheets()

    def _process_sheets(self) -> None:
        wb: OpenpyxlWorkbook = load_workbook(self.template_path)
        for ws in self.sheetnames:
            self.sheet_data.append(wb[ws])

    def process(self) -> None:
        self._process_sheets()

    @property
    def project_name(self) -> str:
        return self._project.name

    def _get_sheets(self) -> None:
        wb = load_workbook(self.template_path)
        self.sheetnames = wb.sheetnames


class WorkSheetFromDatamap:
    def __init__(self, openpyxl_worksheet: OpenpyxlWorksheet, datamap: Datamap) -> None:
        self._data: dict = {}
        self.openpyxl_worksheet = openpyxl_worksheet
        self.datamap = datamap
        self._convert()

    def __getitem__(self, item):
        return self._data[item]

    def _convert(self) -> None:
        for dml in self.datamap.datamapline_set.all():
            key = dml.key
            value = self.openpyxl_worksheet[dml.cell_ref].value
            self._data[key] = value


def convert_openpyxl_worksheet(
    test_sheet_1_data: OpenpyxlWorksheet, datamap: Datamap
) -> WorkSheetFromDatamap:
    return WorkSheetFromDatamap(test_sheet_1_data, datamap)