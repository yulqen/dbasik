from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button
from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Field
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django.core.validators import FileExtensionValidator
from django.forms import FileField
from django.forms import ModelChoiceField
from django.forms import forms
from django.urls import reverse
from django.utils.safestring import mark_safe

from dbasik.datamap import urls as datamap_urls
from dbasik.register.models import Project
from dbasik.datamap.models import Datamap
from dbasik.returns.models import Return

acceptable_types = ["xlsm"]

file_validator = FileExtensionValidator(
    allowed_extensions=acceptable_types,
    message="Source file needs to have extension .xlsm.",
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
        help_text=mark_safe(
            "Please select an existing return. <a href='/returns/create/'>Create a new Return</a>"
        ),
    )

    datamap = ModelChoiceField(
        queryset=Datamap.objects.all(),
        label="Datamap",
        help_text=mark_safe(
            f"Please select an existing Datamap.<br>If you need to create a new Datamap, do so here: <a href='/datamaps{datamap_create_url}'>Create new Datamap</a>"
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return_item = Return.objects.get(id=self.initial["return_obj"])
        project_being_done = Project.objects.get(id=return_item.project.id)

        cancel_redirect = reverse("templates:list")

        self.helper = FormHelper()
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Fieldset(
                f"Upload a populated template for {project_being_done}",
                "datamap",
                "source_file",
            ),
            Field("return_obj", type="hidden"),
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
