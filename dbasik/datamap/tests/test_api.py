from datamap.models import Datamap, DatamapLine
from django.test import Client, TestCase
from register.models import Tier


class TestDatamapAPIEndpoints(TestCase):
    """
    Tests for datamap API endpoints.
    """

    def setUp(self):
        self.client = Client()
        self.dml1 = DatamapLine(
            datamap=Datamap.objects.create(
                name="Test Datamap 1", tier=Tier.objects.create(name="Tier 1")
            ),
            sheet="Test Sheet",
            cell_ref="A1",
        )
        self.dml2 = DatamapLine(
            datamap=Datamap.objects.create(
                name="Test Datamap 1", tier=Tier.objects.create(name="Tier 1")
            ),
            sheet="Test Sheet",
            cell_ref="A2",
        )
        self.dml1.save()
        self.dml2.save()

    def test_datamaps(self):
        response = self.client.get("/api/datamaps/")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.json()[0]["name"], "Test Datamap 1")

    def test_datamaplines(self):
        response = self.client.get("/api/datamaplines/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[1]["cell_ref"], "A2")
        self.assertEqual(response.json()[1]["data_type"], "Text")  # this is default
