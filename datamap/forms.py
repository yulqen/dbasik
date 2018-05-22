from django import forms
from django.core.validators import FileExtensionValidator
#from django.core.exceptions import ValidationError
from .models import PortfolioFamily, Datamap, DatamapLine
from helpers import acceptable_types

file_validator = FileExtensionValidator(
    allowed_extensions=acceptable_types, message="Needs to be a CSV or Excel file."
)


class UploadDatamap(forms.Form):
    target_datamap = forms.ModelChoiceField(queryset=Datamap.objects.all(), empty_label=None)
    uploaded_file = forms.FileField(validators=[file_validator])
    replace_all_entries = forms.BooleanField(initial=True, required=False)


class CreateDatamapForm(forms.Form):

    name = forms.CharField(max_length=50)
    portfolio_family = forms.ModelChoiceField(queryset=PortfolioFamily.objects.all(), empty_label=None)


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
