from django import forms
from .import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ProjectTypeCreateForm(forms.ModelForm):

    class Meta:
        model = models.ProjectType
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout.append(Submit('save', 'Save'))
