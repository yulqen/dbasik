from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from dbasik.datamap.models import Datamap
from dbasik.datamap.tests.fixtures import csv_correct_headers
from dbasik.register.models import Tier


class CsvUploadViewTest(TestCase):
    """
    Tests the view in the Datamap app responsible for handling the
    uploaded csv file intended to provide data for a Datamap.
    """

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(username="lemon", password="lemonlemon")
        cls.csv_file: str = csv_correct_headers()
        cls.datamap = Datamap.objects.create(
            name="Test Datamap",
            slug="test-datamap-test-tier",
            tier=Tier.objects.create(name="Test Tier"),
        )
        cls.upload_url = f"/datamaps/uploaddatamap/test-datamap-test-tier/"

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("datamaps:uploaddatamap", args=["test-datamap-test-tier"])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "datamap/upload_datamap.html")

    def test_post_should_redirect_to_datamap_list(self):
        self.client.force_login(self.user)
        with open(self.csv_file) as csv_f:
            response = self.client.post(
                reverse("datamaps:uploaddatamap", args=["test-datamap-test-tier"]),
                {'replace_all_entries': 1,
                 'uploaded_file': csv_f}
            )
        self.assertRedirects(response, reverse("datamaps:datamap_detail", args=[self.datamap.slug]))

