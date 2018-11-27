from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button
from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django.core.validators import FileExtensionValidator
from django.forms import FileField
from django.forms import ModelChoiceField
from django.forms import forms
from django.urls import reverse
from django.utils.safestring import mark_safe

from datamap import urls as datamap_urls
from datamap.models import Datamap
from register import urls as register_urls
from register.models import FinancialQuarter
from register.models import Project
from returns.models import Return

acceptable_types = ["xlsm"]

file_validator = FileExtensionValidator(
    allowed_extensions=acceptable_types, message="Needs to be a valid Excel file type."
)


class ProcessPopulatedTemplateForm(forms.Form):
    # we can simply override the field if we want to
    # halfway down on Complete forms from models in docs
    datamap_create_url = reverse(
        "datamap-create", current_app="excelparser", urlconf=datamap_urls
    )
    source_file = FileField(validators=[file_validator])

    return_obj = ModelChoiceField(
        queryset=Return.objects.all(),
        help_text="Please select an exististing return. <a href='/returns/create/'>Create a new Return</a>",
    )

    datamap = ModelChoiceField(
        queryset=Datamap.objects.all(),
        label="Datamap",
        help_text=mark_safe(
            f"Please select an existing Datamap. <a href='/datamaps{datamap_create_url}'>Create new Datamap</a>"
        ),
    )
    financial_quarter = ModelChoiceField(
        queryset=FinancialQuarter.objects.all(),
        label="Financial Quarter",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("templates:list")

        self.helper = FormHelper()
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Fieldset(
                "Process a populated spreadsheet",
                "return_obj",
                "datamap",
                "financial_quarter",
                "source_file",
            ),
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
