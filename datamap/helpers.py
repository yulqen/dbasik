import csv
from typing import Union, TextIO, BinaryIO

from django.core.files import File
from django.db import IntegrityError
from django.forms.utils import ErrorDict

from datamap.forms import CSVForm
from datamap.models import DatamapLine, Datamap


class DatamapLinesFromCSVFactory:
    def __init__(self, datamap: Datamap, csv_file: Union[BinaryIO, File]):
        self.csv = csv_file
        self.datamap = datamap
        self._dmls = []
        self.errors = []

    def process(self):
        reader = csv.DictReader(x.decode('utf-8') for x in self.csv.readlines())
        for line in reader:
            form = CSVForm(line)
            if form.is_valid():
                try:
                    _save_datamapline_in_database_or_throw_integrity_error(self.datamap, **form.cleaned_data)
                except IntegrityError as e:
                    self.errors.append(e)
                    raise IntegrityError
            else:
                self.errors = form.errors
                raise ValueError("Invalid CSV value")
        self.csv.close()
        return self

    def __getitem__(self, item):
        return self._dmls[item]


def _save_datamapline_in_database_or_throw_integrity_error(dm: Datamap, **kwargs):
    try:
        DatamapLine.objects.create(datamap=dm, **kwargs)
    except IntegrityError:
        err_str = _parse_kwargs_to_error_string(kwargs)
        raise IntegrityError(f"{err_str} already appears in Datamap: {dm.name}")


def _parse_kwargs_to_error_string(kwargs: dict) -> str:
    err_lst = []
    err_stmt = []
    for x in kwargs.items(): err_lst.append(x)
    for x in err_lst: err_stmt.append(f"{x[0]}: {x[1]}")
    return " ".join([x for x in err_stmt])
