import csv

from django.db import IntegrityError
from django.test import TestCase

from register.models import Tier
from .fixtures import csv_correct_headers, csv_incorrect_headers
from ..forms import CSVForm
from ..helpers import DatamapLinesFromCSVFactory
from ..models import Datamap


class CSVValidatorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.good_csv_file: str = csv_correct_headers()
        cls.bad_csv_file: str = csv_incorrect_headers()
        cls.dm = Datamap.objects.create(
            name="Test Datamap",
            slug="test-datamap",
            tier=Tier.objects.create(name="Tier 1"),
        )

    def test_form_processes_single_line_from_good_csv(self):
        with open(self.good_csv_file, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            line = next(reader)
            form = CSVForm(line)
            if form.is_valid():
                self.assertTrue(form.cleaned_data["key"], "First row col 1")
            else:
                assert False

    def test_dml_factory_with_good_csv(self):
        factory = DatamapLinesFromCSVFactory(
            datamap=self.dm, csv_file=self.good_csv_file
        )
        datamaplines = factory.process()
        self.assertTrue(datamaplines[0].datamap.name, "Test Datamap")
        self.assertTrue(datamaplines[0].key, "First row col 1")

    def test_dml_factory_validation_method_with_bad_keys(self):
        """
        This tests a condition where the bad keys actually get to the CSVForm.
        :return:
        """
        factory = DatamapLinesFromCSVFactory(
            datamap=self.dm, csv_file=self.bad_csv_file
        )
        with open(self.bad_csv_file, "r") as f:
            reader = csv.DictReader(f)
            with self.assertRaisesMessage(
                TypeError,
                "_process_line() got an unexpected keyword argument 'bad_key'",
            ):
                factory._process_line(**next(reader))

    def test_dml_factory_with_bad_csv(self):
        """
        This tests a condition whereby the bad keys don't even get to CSVForm.
        :return:
        """
        factory = DatamapLinesFromCSVFactory(
            datamap=self.dm, csv_file=self.bad_csv_file
        )
        with self.assertRaises(TypeError):
            factory.process()
