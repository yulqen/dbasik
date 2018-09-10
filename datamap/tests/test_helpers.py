from collections import OrderedDict

from django.test import TestCase

from datamap.models import Datamap
from register.models import Tier
from ..helpers import parse_kwargs_to_error_string


class TestDatamapViewHelpers(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.datamap = Datamap.objects.create(
            name="Test Datamap",
            slug="test-datmap",
            tier=Tier.objects.create(name="Test Tier"),
        )

    def test_parse_to_error_string(self):
        kwargs = OrderedDict(key="Key 1", sheet="Sheet", cell_ref="A1")
        self.assertEqual(
            "Database Error: key: Key 1 sheet: Sheet cell_ref: A1 already appears in Datamap: Test Datamap",
            parse_kwargs_to_error_string(self.datamap, kwargs),
        )

    def test_parse_wrong_order_dict_to_error_string(self):
        csv_dict_items = OrderedDict(key="Key 1", cell_ref="A1", sheet="Sheet")
        csv_dict_items_alt = OrderedDict(cell_ref="A1", key="Key 1", sheet="Sheet")
        with self.assertRaisesMessage(
            ValueError,
            "Expects csv_dict_items parameter to be a dict with ordered keys: key, sheet, cell_ref",
        ):
            parse_kwargs_to_error_string(self.datamap, csv_dict_items)
        with self.assertRaisesMessage(
                ValueError,
                "Expects csv_dict_items parameter to be a dict with ordered keys: key, sheet, cell_ref",
        ):
            parse_kwargs_to_error_string(self.datamap, csv_dict_items_alt)
