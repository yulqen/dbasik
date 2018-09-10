from collections import OrderedDict
from typing import List, Tuple, Any

from datamap.models import Datamap


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
        assert [x[0] for x in err_lst] == ['key', 'sheet', 'cell_ref']
    except AssertionError:
        raise ValueError("Expects csv_dict_items parameter to be a dict with ordered keys: key, sheet, cell_ref")
    for x in err_lst:
        err_stmt.append(f"{x[0]}: {x[1]}")
    return (f"Database Error: {' '.join([x for x in err_stmt])}"
            f" already appears in Datamap: {datamap}")
