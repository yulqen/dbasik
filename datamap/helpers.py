import csv
from typing import Union, TextIO, BinaryIO

from django.core.files import File

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
        return self

    def __getitem__(self, item):
        return self._dmls[item]
