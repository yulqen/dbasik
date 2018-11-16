from django.test import TestCase


class TestExcelParserViews(TestCase):
    def setUp(self):
        self.populated_template = "/home/lemon/code/python/dbasik-dev/dbasik-dftgovernance/excelparser/tests/populated.xlsm"

    def test_view_receives_uploaded_file(self):
        response = self.client.post('/excelparser/process-populated/', {'name': 'test'})
        self.assertEqual(response.status_code, 200)

