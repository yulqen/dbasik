import csv
from typing import Union

from django.db import IntegrityError
from django.test import TestCase

from register.models import Tier
from .fixtures import csv_correct_headers, csv_incorrect_headers, csv_repeating_lines
from ..forms import CSVForm
from ..helpers import DatamapLinesFromCSVFactory
from ..models import Datamap, DatamapLine


class CSVValidatorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.good_csv_file: str = csv_correct_headers()
        cls.bad_csv_file: str = csv_incorrect_headers()
        cls.csv_with_repeating_lines: str = csv_repeating_lines()
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

    def _temp_factory_constructor(
        self, csv_file: str, datamap: Union[None, Datamap] = None
    ):
        f = open(csv_file, "rb")
        if datamap:
            factory = DatamapLinesFromCSVFactory(csv_file=f, datamap=datamap)
        else:
            factory = DatamapLinesFromCSVFactory(csv_file=f, datamap=self.dm)
        return factory

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
        factory = self._temp_factory_constructor(self.good_csv_file)
        datamaplines = factory.process()
        self.assertTrue(datamaplines[0].datamap.name, "Test Datamap")
        self.assertTrue(datamaplines[0].key, "First row col 1")

    def test_errors_available_when_bad_key_csv_sent(self):
        factory = self._temp_factory_constructor(self.bad_csv_file)
        factory.process()
        self.assertTrue(len(factory.errors.keys()) == 3)

    def test_dmls_in_system_are_replaced_by_good_csv(self):
        factory = self._temp_factory_constructor(self.good_csv_file, self.dm_with_dmls)
        self.assertTrue(self.dm_with_dmls.name, "Test Datamap with dmls")
        self.assertTrue(
            self.dm_with_dmls.datamapline_set.get(key__istartswith="Key 0 for "), 0
        )
        factory.process(replace=True)
        self.assertTrue(self.dm_with_dmls.name, "Test Datamap with dmls")
        self.assertEqual(factory[0].key, "First row col 1")

    def test_for_integrity_error(self):
        """
        Need to check for django.db.utils.IntegrityError: UNIQUE constraint failed:
        datamap_datamapline.datamap_id, datamap_datamapline.sheet, datamap_datamapline.cell_ref,
        which was being thrown using datamap_dbasik.csv test file.
        :return:
        """
        factory = self._temp_factory_constructor(self.csv_with_repeating_lines, self.dm_with_dmls)
        with self.assertRaises(IntegrityError):
            factory.process()

