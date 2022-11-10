from django import forms
from django.forms import CharField
from django.urls import reverse

# from django.core.exceptions import ValidationError
from dbasik.datamap.validators import file_validator, cell_ref_validator
from .models import Datamap, DatamapLine
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Submit,
    Layout,
    ButtonHolder,
    Fieldset,
    Button,
    Hidden,
    Field,
)


class CSVForm(forms.ModelForm):
    """
    Used to verify an uploaded CSV file, line-by-line.
    """

    cell_ref = CharField(max_length=10, validators=[cell_ref_validator])

    class Meta:
        model = DatamapLine
        exclude = [
            "datamap",
            "data_type",
            "max_length",
            "required",
        ]  # this is the ForeignKey


class DatamapForm(forms.ModelForm):
    class Meta:
        model = Datamap
        fields = ["name", "active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("datamaps:datamap_list")

        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Field("name"),
            # Field("tier", style="width: 100%;"),
            ButtonHolder(
                Submit("submit", "Submit", css_class="button"),
                Button(
                    "cancel",
                    "Cancel",
                    onclick=f"location.href='{cancel_redirect}';",
                    css_class="button danger",
                ),
            ),
        )


class DatamapLineEditForm(forms.ModelForm):
    class Meta:
        model = DatamapLine
        fields = [
            "datamap",
            "key",
            "data_type",
            "max_length",
            "required",
            "sheet",
            "cell_ref",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("datamaps:datamap_list")

        self.helper = FormHelper()
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Create/Edit DatamapLine",
                "datamap",
                "key",
                "data_type",
                "max_length",
                "required",
                "sheet",
                "cell_ref",
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


class DatamapLineDeleteForm(forms.ModelForm):
    class Meta:
        model = DatamapLine
        fields = ["datamap", "key", "sheet", "cell_ref"]


class DatamapLineForm(forms.ModelForm):
    class Meta:
        model = DatamapLine
        fields = [
            "key",
            "datamap",
            "data_type",
            "max_length",
            "required",
            "sheet",
            "cell_ref",
        ]

    def __init__(self, datamap_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.datamap_id = datamap_id

        cancel_redirect = reverse("datamaps:datamap_list")

        self.helper = FormHelper()
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Enter details:",
                "key",
                "data_type",
                "max_length",
                "required",
                "sheet",
                "cell_ref",
            ),
            Hidden("datamap", self.datamap_id),
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


class UploadDatamap(forms.Form):

    uploaded_file = forms.FileField(validators=[file_validator])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("datamaps:datamap_list")

        self.helper = FormHelper()
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset("Upload Datamap", "uploaded_file"),
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
