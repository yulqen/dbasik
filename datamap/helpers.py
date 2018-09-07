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

    def process(self, replace: bool = False):
        reader = csv.DictReader(x.decode('utf-8') for x in self.csv.readlines())
        for line in reader:
            form = CSVForm(line)
            if form.is_valid():
                if replace:
                    DatamapLine.objects.filter(datamap=self.datamap).delete()
                self._dmls.append(
                    DatamapLine.objects.create(
                        datamap=self.datamap, **form.cleaned_data
                    )
                )
            else:
                self.errors = form.errors
                raise ValueError("Invalid CSV value")
        self.csv.close()
        return self

    def __getitem__(self, item):
        return self._dmls[item]


def _save_in_database_or_throw_integrity_error(dm: Datamap, **kwargs):
    try:
        DatamapLine.objects.create(datamap=dm, **kwargs)
    except IntegrityError:
        vars = kwargs.items()
        error_str = f"{([item[0], item[1]) for item in tuple(kwargs.items())}]}"
        raise IntegrityError(error_str)
