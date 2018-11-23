import datetime

from django.test import TestCase
from excelparser.helpers.financial_year import check_date_in_quarter

from register.models import FinancialQuarter
from ..forms import ProcessPopulatedTemplateForm


class UploadPopulatedTemplateTests(TestCase):
    def setUp(self):
        self.form = ProcessPopulatedTemplateForm()

    def test_form_fields_are_valid(self):
        self.assertTrue(self.form.fields["datamap"].label == "Datamap")
        self.assertTrue(
            self.form.fields["financial_quarter"].label == "Financial Quarter"
        )

        # because we haven't explicitly set label on the source_file or project fields...
        self.assertTrue(
            self.form.fields["source_file"].label == "Source file"
            or self.form.fields["source_file"].label is None
        )
        self.assertTrue(
            self.form.fields["project"].label == "Project"
            or self.form.fields["project"].label is None
        )

    def test_help_text_on_each_field(self):
        self.assertEqual(
            self.form.fields["datamap"].help_text,
            "Please select an existing Datamap. <a href='/datamaps/create/'>Create new Datamap</a>",
        )
        self.assertEqual(
            self.form.fields["project"].help_text,
            "Please select an existing Project. <a href='/register/project/create'> Create new Project </a>",
        )


class TestFinancialQuarterDates(TestCase):
    def setUp(self):
        self.fq1 = FinancialQuarter.objects.create(quarter=1, year=2010)
        self.within_quarter = datetime.date(2010, 4, 4)
        self.outwith_quarter = datetime.date(2010, 7, 1)

    def test_whether_a_date_is_in_a_quarter(self):
        self.assertTrue(check_date_in_quarter(self.within_quarter, self.fq1))

    def test_date_outside_quarter(self):
        self.assertFalse(check_date_in_quarter(self.outwith_quarter, self.fq1))

