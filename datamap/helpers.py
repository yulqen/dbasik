import csv

from django.db import IntegrityError

from datamap.forms import CSVForm
from datamap.models import DatamapLine, Datamap


class DatamapLinesFromCSVFactory:
    def __init__(self, datamap: Datamap, csv_file: str):
        self.csv = csv_file
        self.datamap = datamap
        self._dmls = []

    def _process_line(self, line: dict):
        form = CSVForm(**line)


    def process(self):
        with open(self.csv, "r") as f:
            reader = csv.DictReader(f)
            for line in reader:
                try:
                    self._dmls.append(DatamapLine.objects.create(datamap=self.datamap, **line))
                except ValueError:
                    raise

        return self

    def __getitem__(self, item):
        return self._dmls[item]


