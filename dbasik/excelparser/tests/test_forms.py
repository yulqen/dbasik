import datetime
import pathlib

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from datamap.models import DatamapLine
from excelparser.helpers.financial_quarter import check_date_in_quarter
from factories.datamap_factories import DatamapFactory
from factories.datamap_factories import ProjectFactory

from register.models import FinancialQuarter
from returns.models import Return
from excelparser.forms import ProcessPopulatedTemplateForm


class UploadPopulatedTemplateTests(TestCase):
    def setUp(self):
        # self.populated_template = "/home/lemon/code/python/dbasik-dev/dbasik-dftgovernance/excelparser/tests/populated.xlsm"
        self.populated_template = pathlib.Path(__file__).parent.absolute() / "populated_template.xlsm"
        self.project = ProjectFactory()
        self.datamap = DatamapFactory()
        self.dml1 = DatamapLine.objects.create(datamap=self.datamap)
        self.fq = FinancialQuarter.objects.create(quarter=1, year=2010)
        self.return_obj = Return.objects.create(
            project=self.project, financial_quarter=self.fq
        )
        self.form = ProcessPopulatedTemplateForm(initial={'return_obj': self.return_obj.id})

    def test_form_fields_are_valid(self):
        self.assertTrue(self.form.fields["datamap"].label == "Datamap")

        # # because we haven't explicitly set label on the source_file or project fields...
        # self.assertTrue(
        #     self.form.fields["source_file"].label == "Source file"
        #     or self.form.fields["source_file"].label is None
        # )


    def test_valid_form(self):
        f = open(self.populated_template, "rb")
        data = {
            "return_obj": self.return_obj.id,
            "datamap": self.datamap.id,
        }
        file = {"source_file": SimpleUploadedFile(f.name, f.read())}
        form = ProcessPopulatedTemplateForm(data, file, initial={"return_obj": self.return_obj.id})
        self.assertTrue(form.is_valid())
        f.close()


class TestFinancialQuarterDates(TestCase):
    def setUp(self):
        self.fq1 = FinancialQuarter.objects.create(quarter=1, year=2010)
        self.within_quarter = datetime.date(2010, 4, 4)
        self.outwith_quarter = datetime.date(2010, 7, 1)

    def test_whether_a_date_is_in_a_quarter(self):
        self.assertTrue(check_date_in_quarter(self.within_quarter, self.fq1))

    def test_date_outside_quarter(self):
        self.assertFalse(check_date_in_quarter(self.outwith_quarter, self.fq1))
