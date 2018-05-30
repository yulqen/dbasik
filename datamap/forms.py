from django import forms
from django.core.validators import FileExtensionValidator
from django.urls import reverse
#from django.core.exceptions import ValidationError
from .models import Datamap, DatamapLine
from register.models import Tier
from helpers import acceptable_types
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, Fieldset, Button

file_validator = FileExtensionValidator(
    allowed_extensions=acceptable_types, message="Needs to be a CSV or Excel file."
)


class DatamapForm(forms.ModelForm):

    class Meta:
        model = Datamap
        fields = ['name', 'tier', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse('datamaps:datamap_list')

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                'Create/Edit Datamap',
                'name',
                'tier',
                'active'
            ),
            ButtonHolder(
                Submit('submit', 'Submit'),
                Button('cancel', 'Cancel', onclick=f"location.href='{cancel_redirect}';", css_class="btn btn-danger")
            )
        )


class CreateDatamapLineForm(forms.ModelForm):

    class Meta:
        model = DatamapLine
        exclude = ['datamap']


class UploadDatamap(forms.Form):
    target_datamap = forms.ModelChoiceField(queryset=Datamap.objects.all(), empty_label=None)
    uploaded_file = forms.FileField(validators=[file_validator])
    replace_all_entries = forms.BooleanField(initial=True, required=False)


class CreateDatamapForm(forms.Form):

    name = forms.CharField(max_length=50)
    tier = forms.ModelChoiceField(queryset=Tier.objects.all(), empty_label=None)


class EditDatamapLineForm(forms.ModelForm):

    class Meta:
        model = DatamapLine
        exclude = ['datamap']
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
