from django.core.exceptions import ValidationError
from django.test import TestCase

from datamap.forms import CSVForm


class DatamapFormsTests(TestCase):

    def test_max_chars_based_on_model(self):
        long_key = "A" * 101
        long_sheet = "A" * 51
        long_cell_ref = "A" * 11

        form = CSVForm(data={"key": long_key, "sheet": "Summary", "cell_ref": "A10"})
        self.assertFalse(form.is_valid())

        form = CSVForm(data={"key": "A", "sheet": long_sheet, "cell_ref": "A10"})
        self.assertFalse(form.is_valid())

        form = CSVForm(data={"key": "A", "sheet": "A", "cell_ref": long_cell_ref})
        self.assertFalse(form.is_valid())

    def test_csv_form_excludes_datamap(self):
        form = CSVForm()
        with self.assertRaises(KeyError):
            form.fields["datamap"]

    def test_csv_form(self):
        form = CSVForm()
        self.assertTrue(form.fields["key"].label is None or form.fields["key"])
