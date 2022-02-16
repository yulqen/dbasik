from django.test import TestCase

from templates.models import Template, TemplateDataLine


class TemplateModelTests(TestCase):
    def setUp(self):
        self.template = Template.objects.create(
            name="Test",
            description="Description",
            source_file="/home/lemon/code/python/dbasik-dev/dbasik-dftgovernance/templates/tests/macro_enabled_template.xlsm",
        )
        self.data = TemplateDataLine.objects.create(
            template=self.template, sheet="Test Sheet", cellref="A1", value="Test Value"
        )

    def test_basic_model(self):
        self.assertEqual(self.template.name, "Test")
        self.assertEqual(
            self.template.source_file,
            "/home/lemon/code/python/dbasik-dev/dbasik-dftgovernance/templates/tests/macro_enabled_template.xlsm",
        )

    def test_template_data(self):
        self.assertEqual(
            self.template.data.get(cellref="A1").value, "Test Value"
        )
