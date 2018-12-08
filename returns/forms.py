from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, ButtonHolder, Fieldset, Layout, Submit
from django import forms
from django.forms import ModelChoiceField
from django.urls import reverse

from datamap.models import Datamap
from register.models import FinancialQuarter, Project

from . import models


class ReturnBatchCreateForm(forms.Form):

    financial_quarter = forms.ModelChoiceField(
        queryset=FinancialQuarter.objects.all(), help_text="Choose a Financial Quarter"
    )
    datamap = forms.ModelChoiceField(
        queryset=Datamap.objects.all(), help_text="Choose a datamap"
    )
    source_files = forms.FileField(
        help_text="Please ensure the name of each file matches exactly the title of the project!",
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("returns:returns_list")

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset("Create new Returns (batch upload)", "financial_quarter", "datamap", "source_files"),
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


class ReturnCreateForm(forms.ModelForm):

    project = ModelChoiceField(
        queryset=Project.objects.all(),
        help_text="Please select an existing Project. <a href='/register/project/create' target='_blank'>Create a new "
        "Project</a>",
    )

    class Meta:
        model = models.Return
        fields = ["project", "financial_quarter"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("returns:returns_list")

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset("Create new Return", "project", "financial_quarter"),
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
