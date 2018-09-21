from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button
from django.core.validators import FileExtensionValidator
from django.forms import forms, FileField, ModelChoiceField, ChoiceField
from django.urls import reverse

from datamap.models import Datamap
from register.models import Project

acceptable_types = ["xlsm"]

file_validator = FileExtensionValidator(
    allowed_extensions=acceptable_types, message="Needs to be a valid Excel file type."
)

class ProcessPopulatedTemplateForm(forms.Form):
    # we can simply override the field if we want to
    # halfway down on Complete forms from models in docs
    source_file = FileField(validators=[file_validator])
    project = ModelChoiceField(queryset=Project.objects.all())
    datamap = ModelChoiceField(queryset=Datamap.objects.all())
    financial_quarter = ChoiceField(choices=[('test', 'TEST')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("templates:list")

        self.helper = FormHelper()
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Fieldset("Process a populated spreadsheet", "datamap", "project", "financial_quarter", "source_file"),
            ButtonHolder(
                Submit("submit", "Submit"),
                Button(
                    "cancel",
                    "Cancel",
                    onclick=f"location.href='{cancel_redirect}';",
                    css_class="btn btn-danger",
                ),
            ),
        )
