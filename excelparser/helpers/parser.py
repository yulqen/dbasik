import datetime
from enum import Enum
from enum import auto
from typing import Any
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Union

from openpyxl import load_workbook
from openpyxl import Workbook as OpenpyxlWorkbook
from openpyxl.worksheet import Worksheet as OpenpyxlWorksheet

from datamap.models import Datamap
from register.models import FinancialQuarter
from register.models import Project

SheetData = Dict[str, "WorkSheetFromDatamap"]


class MissingSheetError(Exception):
    pass


class ParsedSpreadsheet:
    """
    A single spreadsheet whose data can be extracted using a Datamap upon
    calling the process() method. Data per sheet is then available via
    a processed_spreadsheet['sheet_name'] basis.
    """

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
        self.sheet_data: SheetData = {}
        self.sheetnames: List[str]
        self._get_sheets()
        self._dml_sheets: List[str]
        self._dml_sheets_missing_from_spreadsheet: List[str]
        self._check_sheets_present()

    def __getitem__(self, item):
        return self.sheet_data[item]

    def _check_sheets_present(self) -> None:
        dmls = self.datamap.datamapline_set.all()
        self._dml_sheets = list({dml.sheet for dml in dmls})
        if list(set(self.sheetnames) - set(self._dml_sheets)):
            raise MissingSheetError("There is a worksheet in the spreadsheet not in the Datamap")

    def _process_sheets(self) -> None:
        wb: OpenpyxlWorkbook = load_workbook(self.template_path)
        for ws in self.sheetnames:
            ws_from_dm = WorkSheetFromDatamap(
                openpyxl_worksheet=wb[ws], datamap=self.datamap
            )
            ws_from_dm._convert()
            self.sheet_data[ws] = ws_from_dm

    def process(self) -> None:
        self._process_sheets()

    @property
    def project_name(self) -> str:
        return self._project.name

    def _get_sheets(self) -> None:
        wb = load_workbook(self.template_path)
        self.sheetnames = wb.sheetnames


class CellValueType(Enum):
    """
    Type classifiers for data parsed from a spreadsheet.
    """

    INTEGER = auto()
    STRING = auto()
    DATE = auto()
    DATETIME = auto()
    FLOAT = auto()
    UNKNOWN = auto()


class CellData(NamedTuple):
    """
    Holds the data and useful metadata parsed from a spreadsheet.
    """

    key: str
    sheet: str
    value: str
    source_cell: str
    type: Any


class WorkSheetFromDatamap:
    """
    A dictionary-like object holding the data for a single spreadsheet sheet
    parsed using a Datamap object. Created by calling process() method on a
    ParsedSpreadsheet object.
    """

    def __init__(self, openpyxl_worksheet: OpenpyxlWorksheet, datamap: Datamap) -> None:
        self._data: Dict[str, CellData] = {}
        self.openpyxl_worksheet = openpyxl_worksheet
        self.datamap = datamap
        self._convert()

    def __getitem__(self, item):
        return self._data[item]

    def _convert(self) -> None:
        """
        Populates self._data dictionary with data from the spreadsheet.
        If type of data is not expected (i.e. not in the enum CellValueType)
        will still parse the data but classify it as CellValueType.UNKOWN
        for onward processing.
        :return: None
        :rtype: None
        """
        for _dml in self.datamap.datamapline_set.filter(
            sheet__exact=self.openpyxl_worksheet.title
        ):
            _key = _dml.key
            _parsed_value = self.openpyxl_worksheet[_dml.cell_ref].value
            _sheet_title = self.openpyxl_worksheet.title
            try:
                _value = CellData(
                    _key,
                    _sheet_title,
                    _parsed_value,
                    _dml.cell_ref,
                    _detect_cell_type(_parsed_value),
                )
                self._data[_key] = _value
            except ValueError:
                _value = CellData(
                    _key,
                    _sheet_title,
                    _parsed_value,
                    _dml.cell_ref,
                    CellValueType.UNKNOWN,
                )
                self._data[_key] = _value


def _detect_cell_type(obj: Any) -> CellValueType:
    """
    Takes an object and maps its type to the CellValueType enum.
    Raises ValueError exception if the object is not an enum type
    useful for this process (int, str, float, etc).
    :param obj:
    :type obj: List[str]
    :return: CellValueType
    :rtype: None
    """
    if isinstance(obj, int):
        return CellValueType.INTEGER
    if isinstance(obj, str):
        return CellValueType.STRING
    if isinstance(obj, float):
        return CellValueType.FLOAT
    if isinstance(obj, datetime.datetime):
        return CellValueType.DATETIME
    else:
        raise ValueError("Cannot detect applicable type")
