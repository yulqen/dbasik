from dbasik.datamap.models import Datamap, DatamapLine
from dbasik.register.models import Tier
from django.test import Client, TestCase


class TestDatamapAPIEndpoints(TestCase):
    """
    Tests for datamap API endpoints.
    """

    def setUp(self):
        self.client = Client()
        self.datamap = Datamap.objects.create(
            name="Test Datamap 1")
        self.dml1 = DatamapLine.objects.create(
            datamap=self.datamap,
            key="Test 1",
            sheet="Test Sheet",
            cell_ref="A1",
        )
        self.dml2 = DatamapLine.objects.create(
            key="Test 1",
            datamap=self.datamap,
            sheet="Test Sheet",
            cell_ref="A2",
        )
        self.dml1.save()
        self.dml2.save()

    def test_datamaps(self):
        response = self.client.get("/api/datamap/datamaps")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.json()[0]["name"], "Test Datamap 1")

    def test_datamaplines(self):
        response = self.client.get("/api/datamap/datamap?slug=test-datamap-1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["cell_ref"], "A1")
        self.assertEqual(response.json()[1]["cell_ref"], "A2")
        self.assertEqual(response.json()[0]["data_type"], "Text")  # this is default
        self.assertEqual(
            response.json()[0]["datamap"]["slug"], "test-datamap-1"
        )  # this is default
