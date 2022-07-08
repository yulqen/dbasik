from collections import OrderedDict

from django.test import TestCase

from dbasik.datamap.models import Datamap
from dbasik.register.models import Tier

from ..helpers import parse_kwargs_to_error_string


class TestDatamapViewHelpers(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.csv_dict_items_correct = OrderedDict(key="Key 1", sheet="Sheet", cell_ref="A1")
        cls.csv_dict_items_incorrect_1 = OrderedDict(cell_ref="A1", key="Key 1", sheet="Sheet")
        cls.csv_dict_items_incorrect_2 = OrderedDict(key="Key 1", cell_ref="A1", sheet="Sheet")
        cls.datamap = Datamap.objects.create(
            name="Test Datamap",
            slug="test-datamap",
            tier=Tier.objects.create(name="Test Tier"),
        )
        cls.expected_message = (
            "Database Error: key: Key 1 sheet: Sheet cell_ref: "
            "A1 already appears in this Datamap"
        )
        cls.exception_message = (
            "Expects csv_dict_items parameter to be a dict with "
            "ordered keys: key, sheet, cell_ref"
        )

    def test_parse_to_error_string(self):
        self.assertEqual(
            self.expected_message, parse_kwargs_to_error_string(self.datamap, self.csv_dict_items_correct)
        )

    def test_parse_wrong_order_dict_to_error_string(self):
        with self.assertRaisesMessage(ValueError, self.exception_message):
            parse_kwargs_to_error_string(self.datamap, self.csv_dict_items_incorrect_1)
        with self.assertRaisesMessage(ValueError, self.exception_message):
            parse_kwargs_to_error_string(self.datamap, self.csv_dict_items_incorrect_2)
