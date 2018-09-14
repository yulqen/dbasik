from django.core.exceptions import ValidationError
from django.test import TestCase

from datamap.models import DatamapLine, Datamap
from register.models import Tier


class DatamapModelTests(TestCase):
    def test_bad_cell_ref(self):
        dml = DatamapLine(
            datamap=Datamap.objects.create(
                name="Test Datamap 1", tier=Tier.objects.create(name="Tier 1")
            ),
            sheet="Test Sheet",
            cell_ref="NOT ALLOWED",
        )
        with self.assertRaises(ValidationError):
            dml.full_clean()
