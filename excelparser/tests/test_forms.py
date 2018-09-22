from django.test import TestCase

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
        self.assertTrue(
            self.form.fields["datamap"].help_text
            == "Please select an existing Datamap. <a href='#'>Create new Datamap</a>"
        )
