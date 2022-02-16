from django import forms
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.forms import FileField

from .models import Template
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, Fieldset, Button, Hidden

acceptable_types = ["xlsm"]


file_validator = FileExtensionValidator(
    allowed_extensions=acceptable_types, message="Needs to be a valid Excel file type."
)


class TemplateCreateForm(forms.ModelForm):

    # we can simply override the field if we want to
    # halfway down on Complete forms from models in docs
    source_file = FileField(validators=[file_validator])

    class Meta:
        model = Template
        fields = ["name", "description", "source_file"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("templates:list")

        self.helper = FormHelper()
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Fieldset("Create new Template", "name", "description", "source_file"),
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
