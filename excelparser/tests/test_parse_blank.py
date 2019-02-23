import os

from django.test import TestCase

from excelparser.helpers.parser import ParsedBlankTemplate
from templates.models import Template


class ParseBlankSpreadsheet(TestCase):
    @classmethod
    def setUpTestData(cls):
        code_dir = os.path.abspath('.')
        cls.blank = os.path.join(code_dir, 'templates/tests/macro_enabled_template.xlsm')
        cls.tmpl = Template.objects.create(name="Test Template", source_file=cls.blank)

    def test_parse_blank_template(self):
        parsed = ParsedBlankTemplate(self.blank)
        self.assertEqual(parsed["Test Sheet"][0]["A1"], "Col A Key 1")
