import csv
import os
import tempfile

from django.core.files.uploadedfile import UploadedFile
from django.test import TestCase

from datamap.helpers import check_duplicate_lines


class TestDuplicateCSVLines(TestCase):
    def setUp(self):
        TEMPDIR = tempfile.gettempdir()
        self.df: str = os.path.join(TEMPDIR, "csv_repeating_lines.csv")
        with open(self.df, "w") as f:
            f.write("cell_key,template_sheet,cell_reference\n")
            f.write("First row col 1,Sheetname,A15\n")
            f.write("Second row col 1,Sheetname,A15\n")
            f.write("Third row col 1,Other Sheetname,A16\n")
            self.expected_str = (
                "Check duplicated lines:\n"
                "Second row col 1: Sheetname, A15\n"
            )

    def test_duplicate_lines(self):
        dup_str = check_duplicate_lines(self.df)
        self.assertEqual(dup_str, self.expected_str)


class TestDuplicateMultiCSVLines(TestCase):
    def setUp(self):
        TEMPDIR = tempfile.gettempdir()
        self.df: str = os.path.join(TEMPDIR, "csv_repeating_lines.csv")
        with open(self.df, "w") as f:
            f.write("cell_key,template_sheet,cell_reference\n")
            f.write("First row col 1,Sheetname,A15\n")
            f.write("Second row col 1,Sheetname,A15\n")
            f.write("Third row col 1,Other Sheetname,A16\n")
            f.write("Fourth row col 1,Sheetname,A15\n")
            self.expected_str = (
                "Check duplicated lines:\n"
                "Second row col 1: Sheetname, A15\n"
                "Fourth row col 1: Sheetname, A15\n"
            )

    def test_duplicate_lines(self):
        dup_str = check_duplicate_lines(self.df)
        self.assertEqual(dup_str, self.expected_str)


def test_good_csv_file(good_csv_file):
    with open(good_csv_file, "r") as f:
        uf = UploadedFile(f)
        csv_reader = csv.DictReader(uf)
        line = next(csv_reader)
        assert line["key"] == "First row col 1"
        assert line["sheet"] == "First row col 2"
        assert line["cell_ref"] == "A15"
        line = next(csv_reader)
        assert line["key"] == "Second row col 1"
        assert line["sheet"] == "Second row col 2"
        assert line["cell_ref"] == "B15"


def test_csv_contents(uploaded_csv_file):
    uf = UploadedFile(uploaded_csv_file)
    csv_reader = csv.DictReader(uf)
    line = next(csv_reader)
    assert line["key"] == "First row col 1UL"
    assert line["sheet"] == "First row col 2UL"
    assert line["cell_ref"] == "A15"
    line = next(csv_reader)
    assert line["key"] == "Second row col 1UL"
    assert line["sheet"] == "Second row col 2UL"
    assert line["cell_ref"] == "B15"
