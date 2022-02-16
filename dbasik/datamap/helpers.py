import csv

from collections import OrderedDict, Counter
from typing import List, Tuple, Any, Set, Dict

from datamap.models import Datamap


class _DataLine:
    def __init__(self, key, sheet, cell_ref):
        self.key = key
        self.sheet = sheet
        self.cell_ref = cell_ref

    def __hash__(self):
        return hash((self.sheet, self.cell_ref))

    def __eq__(self, value):
        if (self.sheet, self.cell_ref) == value:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.key} - {self.sheet}, {self.cell_ref}"

    def __repr__(self):
        return f"{self.key} - {self.sheet}, {self.cell_ref}"


def check_duplicate_lines(f_path: str):
    with open(f_path, "r") as f:
        csv_reader = csv.DictReader(f)
        _data_lines = []
        for line in csv_reader:
            _data_lines.append(_DataLine(line["cell_key"], line["template_sheet"], line["cell_reference"]))
        s = list(set(_data_lines))
        for x in s:
            _data_lines.remove(x)

        _intro = "Check duplicated lines:\n"
        return "".join([_intro, *[f"{x.key}: {x.sheet}, {x.cell_ref}\n" for x in _data_lines]])


def parse_kwargs_to_error_string(datamap: Datamap, csv_dict_items: OrderedDict) -> str:
    """
    Parses the items from a csv.DictReader line into an error message to be used
    by a exception elsewhere. Will raise ValueError if keys for csv_dict_items
    do not match ["key", "sheet", "cell_ref"]. As csv.DictReader uses an OrderedDict,
    this should be a given, but we rely on that order to it is flagged.

    :param datamap:
    :type datamap: datamap.models.Datamap
    :param csv_dict_items:
    :type csv_dict_items: collections.OrderedDict
    :return: the message
    :rtype: str
    """
    err_lst: List[Tuple[Any, Any]] = []
    err_stmt = []
    x: Tuple[Any, Any]
    for x in csv_dict_items.items():
        err_lst.append(x)
    try:
        assert [x[0] for x in err_lst] == ["key", "sheet", "cell_ref"]
    except AssertionError:
        raise ValueError(
            "Expects csv_dict_items parameter to be a dict with ordered keys: key, sheet, cell_ref"
        )
    for x in err_lst:
        err_stmt.append(f"{x[0]}: {x[1]}")
    return (
        f"Database Error: {' '.join([x for x in err_stmt])}" f" already appears in this Datamap"
    )
