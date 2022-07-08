import os
import tempfile

from django.test import TestCase

from dbasik.datamap.helpers import check_duplicate_lines


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
