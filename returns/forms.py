from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button
from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelChoiceField
from django.urls import reverse

from register.models import Project
from . import models


class ReturnCreateForm(forms.ModelForm):

    project = ModelChoiceField(
        queryset=Project.objects.all(),
        help_text="Please select an existing Project. <a href='/register/project/create' target='_blank'>Create a new "
                  "Project</a>",
    )

    class Meta:
        model = models.Return
        fields = ['project', 'financial_quarter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse('returns:returns_list')

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                'Create new Return',
                'project',
                'financial_quarter',
            ),
            ButtonHolder(
                Submit('submit', 'Submit'),
                Button('cancel', 'Cancel', onclick=f"location.href='{cancel_redirect}';", css_class="btn btn-danger")
            )
        )

