from django import forms
from django.forms import ModelChoiceField
from django.urls import reverse

from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, Fieldset, Button


class ReturnCreateForm(forms.ModelForm):
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

