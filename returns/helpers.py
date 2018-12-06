from typing import List

from openpyxl import Workbook
from openpyxl import utils

from register.models import FinancialQuarter
from datamap.models import Datamap


def generate_master(financial_quarter: FinancialQuarter, output: str, datamap: Datamap):
    # we need to get all returns for a FinancialQuarter
    all_returns = financial_quarter.return_financial_quarters.all()
    keys: List = [dml.key for dml in datamap.datamaplines.all()]
    wb = Workbook()
    ws = wb.active

    # do the key column
    for row in range(1, len(keys) + 1):
        ws.cell(column=1, row=row, value=keys[row - 1])

    column_counter = 2  # start at column 2 after the key column
    for ret in all_returns:
        ret_items = ret.return_returnitems.all()
        for counter_through_items, item in enumerate(ret_items, start=1):
            ws.cell(column=column_counter, row=counter_through_items, value=item.value_str)
        column_counter += 1
    ws.title = "Master Data"
    dest_filename = "master.xlsm"
    wb.save(filename=dest_filename)
