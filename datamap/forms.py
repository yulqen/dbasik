from django import forms
from django.core.validators import FileExtensionValidator
from django.urls import reverse

# from django.core.exceptions import ValidationError
from .models import Datamap, DatamapLine
from register.models import Tier
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, Fieldset, Button, Hidden

acceptable_types = {
    "csv": ["text/csv"],
    "xlsx": ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
    "xlsm": [
        "application/vnd.ms-excel.sheet.macroEnabled.12",
        "application/vnd.ms-excel.sheet.macroenabled.12",
    ],
}


file_validator = FileExtensionValidator(
    allowed_extensions=acceptable_types, message="Needs to be a CSV or Excel file."
)


class CSVForm(forms.ModelForm):
    """
    Used to verify an uploaded CSV file, line-by-line.
    """

    class Meta:
        model = DatamapLine
        exclude = ["datamap"]  # this is the ForeignKey


class DatamapForm(forms.ModelForm):

    class Meta:
        model = Datamap
        fields = ["name", "tier", "active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("datamaps:datamap_list")

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset("Create/Edit Datamap", "name", "tier", "active"),
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


class DatamapLineForm(forms.ModelForm):

    class Meta:
        model = DatamapLine
        fields = ["datamap", "key", "sheet", "cell_ref"]

    def __init__(self, datamap_id, *args, **kwargs):
        self.datamap_id = datamap_id
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("datamaps:datamap_list")

        self.helper = FormHelper()
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset("Create/Edit DatamapLine", "key", "sheet", "cell_ref"),
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

    def __init__(self, datamap_id, *args, **kwargs):
        self.datamap_id = datamap_id
        super().__init__(*args, **kwargs)

        #       cancel_redirect = reverse('datamaps:datamap_list')

        self.helper = FormHelper()
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Upload Datamap",
                "uploaded_file",
                "replace_all_entries",
            ),
            Hidden("target_datamap", self.datamap_id),
            ButtonHolder(
                Submit("submit", "Submit"),
                # Button('cancel', 'Cancel', onclick=f"location.href='{cancel_redirect}';", css_class="btn btn-danger")
            ),
        )

    target_datamap = forms.ModelChoiceField(
        queryset=Datamap.objects.all(), empty_label=None
    )
    uploaded_file = forms.FileField(validators=[file_validator])
    replace_all_entries = forms.BooleanField(initial=True, required=False)


class EditDatamapLineForm(forms.ModelForm):

    class Meta:
        model = DatamapLine
        exclude = ["datamap"]


# HOW TO WRITE A CUSTOM CLEAN FUNCTION IN FORM
# it must be of form clean_<attribute>(self) and
# return the cleaned data or a ValidationError exception
# see Django Unleased: https://www.safaribooksonline.com/library/view/django-unleashed/9780133812497/ch07lev2sec4.html
# 7.3.5:
#    def clean_sheet(self):
#        if self.cleaned_data['sheet'] in ['Summary']:
#            return self.cleaned_data['sheet']
#        else:
#            raise ValidationError("No..!")
