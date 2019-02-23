import os

from templates.models import Template

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase


def mock_macro_template():
    code_dir = os.path.abspath('.')
    return os.path.join(code_dir, 'templates/tests/macro_enabled_template.xlsm')


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(email="baws@baws.com", username="bawsbaws", password="tuplips901")
        cls.mock_template_file: str = mock_macro_template()
        cls.tmpl = Template.objects.create(name="Test Template", source_file=cls.mock_template_file)
        cls.client = Client()


    def test_new_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("templates:create"))
        self.assertEqual(response.status_code, 200)


    def test_template_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("templates:list"))
        self.assertEqual(response.status_code, 200)


    def test_template_detail_basic(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("templates:template_detail", args=[self.tmpl.slug]))
        self.assertEqual(response.status_code, 200)

    def test_post_should_redirect_to_template_list(self):
        self.client.force_login(self.user)
        with open(self.mock_template_file, "rb") as template_f:
            response = self.client.post(
                reverse("templates:create"),
                {'name': "Test Template",
                 'descripton': "Test Description",
                 'source_file': template_f}
            )
        self.assertEqual(response.status_code, 200)
        list_response = self.client.get(reverse("templates:list"))
        self.assertContains(list_response, "Test Template", html=True)


    def test_template_detail(self):
        self.client.force_login(self.user)
        with open(self.mock_template_file, "rb") as template_f:
            response = self.client.post(
                reverse("templates:create"),
                {'name': "Test Template",
                 'descripton': "Test Description",
                 'source_file': template_f}
            )
        self.assertEqual(response.status_code, 200)
        detail_response = self.client.get(reverse("templates:template_detail", args=["test-template"]))
        self.assertEqual(detail_response.status_code, 200)
        a1_cell_dict = {"cellref": "A1", "value": "Col A Key 1"}
        self.assertEqual(detail_response.context["submitted_template"][0]["Test Sheet"][0], a1_cell_dict)
