import csv
from django.test import TestCase

from datamap.models import Datamap
from datamap.tests.fixtures import csv_correct_headers
from register.models import Tier
from datamap.forms import CSVForm
from ..helpers import DatamapLinesFromCSVFactory


class CSVValidatorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.csv_file: str = csv_correct_headers()

    def test_form_exists(self):
        form = CSVForm()
        self.assertTrue(form, True)

    def test_form_processes_single_line_from_csv(self):
        with open(self.csv_file, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            line = next(reader)
            form = CSVForm(line)
            if form.is_valid():
                self.assertTrue(form.cleaned_data["key"], "First row col 1")
            else:
                assert False

    def test_dml_factory_with_good_csv(self):
        dm = Datamap.objects.create(
            name="Test Datamap",
            slug="test-datamap",
            tier=Tier.objects.create(name="Tier 1"),
        )
        factory = DatamapLinesFromCSVFactory(datamap=dm, csv_file=self.csv_file)
        datamaplines = factory.process()
        self.assertTrue(datamaplines[0].datamap.name, "Test Datamap")
        self.assertTrue(datamaplines[0].key, "First row col 1")
