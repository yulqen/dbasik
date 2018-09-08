import csv
from typing import Union

from django.db import IntegrityError
from django.test import TestCase

from datamap.helpers import _save_or_except
from register.models import Tier
from .fixtures import csv_correct_headers, csv_incorrect_headers, csv_repeating_lines
from .fixtures import csv_containing_hundred_plus_length_key as csv_long_key
from ..forms import CSVForm
from ..helpers import DatamapLinesFromCSV
from ..models import Datamap, DatamapLine


class CSVValidatorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.good_csv_file: str = csv_correct_headers()
        cls.bad_csv_file: str = csv_incorrect_headers()
        cls.csv_with_repeating_lines: str = csv_repeating_lines()
        cls.long_key_csv: str = csv_long_key()
        cls.dm = Datamap.objects.create(
            name="Test Datamap",
            slug="test-datamap",
            tier=Tier.objects.create(name="Tier 1"),
        )
        cls.dm_with_dmls = Datamap.objects.create(
            name="Old datamap with dmls",
            slug="old-datamap-with-dmls",
            tier=Tier.objects.create(name="Tier 1"),
        )
        # create a bunch of DatamapLine objects for cls.dm_with_dmls
        for x in range(10):
            DatamapLine.objects.create(
                datamap=cls.dm_with_dmls,
                key=f"Key {x} for {cls.dm_with_dmls.__class__}",
                sheet=f"Sheetname for {cls.dm_with_dmls.__class__}",
                cell_ref=f"A{x}",
            )
        cls.dm_with_repeating_lines = Datamap.objects.create(
            name="Repeating datamap with dmls",
            slug="repeating-datamap-with-dmls",
            tier=Tier.objects.create(name="Tier 1"),
        )
        # create a bunch of DatamapLine objects for cls.dm_with_repeating_lines
        for x in range(10):
            DatamapLine.objects.create(
                datamap=cls.dm_with_repeating_lines,
                key=f"Key {x} for {cls.dm_with_repeating_lines.__class__}",
                sheet=f"Sheetname for {cls.dm_with_repeating_lines.__class__}",
                cell_ref=f"A{x}",
            )

    def _setup(
        self, csv_file: str, datamap: Union[None, Datamap] = None
    ):
        f = open(csv_file, "rb")
        if datamap:
            datamaplines_from_csv = DatamapLinesFromCSV(csv_file=f, datamap=datamap)
        else:
            datamaplines_from_csv = DatamapLinesFromCSV(csv_file=f, datamap=self.dm)
        return datamaplines_from_csv

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
        datamaplines_from_csv = self._setup(self.good_csv_file)
        datamaplines = datamaplines_from_csv.process()
        self.assertTrue(datamaplines[0].datamap.name, "Test Datamap")
        self.assertTrue(datamaplines[0].key, "First row col 1")

    def test_correct_number_of_dmls_in_dm_matching_csv(self):
        datamaplines_from_csv = self._setup(self.good_csv_file)
        datamaplines = datamaplines_from_csv.process()
        with open(self.good_csv_file, 'r') as f:
            len_csv = len(f.readlines())
        self.assertEqual(len(datamaplines), len_csv - 1)

    def test_errors_available_when_bad_key_csv_sent(self):
        datamaplines_from_csv = self._setup(self.bad_csv_file)
        with self.assertRaisesMessage(ValueError, "Invalid CSV value"):
            datamaplines_from_csv.process()

    def test_dmls_in_system_are_replaced_by_good_csv(self):
        datamaplines_from_csv = self._setup(self.good_csv_file, self.dm_with_dmls)
        self.assertEqual(self.dm_with_dmls.name, "Old datamap with dmls")
        self.assertTrue(
            self.dm_with_dmls.datamapline_set.get(key__istartswith="Key 0 for "), 0
        )
        datamaplines_from_csv.process()
        self.assertEqual(self.dm_with_dmls.name, "Old datamap with dmls")
        self.assertEqual(datamaplines_from_csv[0].key, "First row col 1")

    def test_for_integrity_error(self):
        """
        Need to check for django.db.utils.IntegrityError: UNIQUE constraint failed:
        datamap_datamapline.datamap_id, datamap_datamapline.sheet, datamap_datamapline.cell_ref,
        which was being thrown using datamap_dbasik.csv test file.
        :return:
        """
        datamaplines_from_csv = self._setup(
            self.csv_with_repeating_lines, self.dm_with_dmls
        )
        with self.assertRaises(IntegrityError):
            datamaplines_from_csv.process()

    def test_save_in_database_or_throw_integrity_error(self):
        dm = Datamap.objects.create(name="Test Datamap", tier=Tier.objects.create(name="Tier 1"), slug="test-datamap")
        DatamapLine.objects.create(datamap=dm, key="Key 1", cell_ref="A1")
        with self.assertRaisesMessage(
            IntegrityError,
            "key: Key 1 cell_ref: A1 already appears in Datamap: Test Datamap",
        ):
            _save_or_except(
                dm, key="Key 1", cell_ref="A1"
            )

    def test_for_invalid_csv_line(self):
        datamaplines_from_csv = self._setup(self.long_key_csv, self.dm)
        with self.assertRaisesMessage(ValueError, "Invalid CSV value"):
            datamaplines_from_csv.process()

    def test_database_stays_same_even_after_bad_csv(self):
        datamaplines_from_csv = self._setup(self.bad_csv_file, self.dm_with_dmls)
        self.assertEqual(self.dm_with_dmls.name, "Old datamap with dmls")
        self.assertTrue(
            self.dm_with_dmls.datamapline_set.get(key__istartswith="Key 0 for "), 0
        )
        with self.assertRaisesMessage(ValueError, "Invalid CSV value"):
            datamaplines_from_csv.process()
        self.assertEqual(self.dm_with_dmls.name, "Old datamap with dmls")
        self.assertTrue(
            self.dm_with_dmls.datamapline_set.get(key__istartswith="Key 0 for "), 0)
