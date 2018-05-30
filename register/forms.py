from django import forms
from django.urls import reverse
from .import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, Fieldset, Button


class TierForm(forms.ModelForm):

    class Meta:
        model = models.Tier
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse('register:tier_list')

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                'Create/Edit Tier',
                'name',
                'description',
            ),
            ButtonHolder(
                Submit('submit', 'Submit'),
                Button('cancel', 'Cancel', onclick=f"location.href='{cancel_redirect}';", css_class="btn btn-danger")
            )
        )


class ProjectTypeForm(forms.ModelForm):

    class Meta:
        model = models.ProjectType
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse('register:projecttype_list')

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                'Create/Edit Project Type',
                'name',
                'description',
            ),
            ButtonHolder(
                Submit('submit', 'Submit'),
                Button('cancel', 'Cancel', onclick=f"location.href='{cancel_redirect}';", css_class="btn btn-danger")
            )
        )
