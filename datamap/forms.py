from django import forms
from django.core.validators import FileExtensionValidator
from .models import PortfolioFamily
from helpers import CSVUploadedFile # change this

file_validator = FileExtensionValidator(
    allowed_extensions=CSVUploadedFile.acceptable_types,
    message='Needs to be a CSV or Excel file.')


class UploadDatamap(forms.Form):
    file_name = forms.CharField(max_length=30)
    uploaded_file = forms.FileField(validators=[file_validator])


class CreateDatamapForm(forms.Form):

    pfs = PortfolioFamily.objects.all()

    name = forms.CharField(max_length=50)
    portfolio_family = forms.ChoiceField(
        choices=[(p.id, p.name) for p in pfs]
    )
