from django import forms
from .models import PortfolioFamily


class UploadDatamap(forms.Form):
    file_name = forms.CharField(max_length=30)
    uploaded_file = forms.FileField()


class CreateDatamapForm(forms.Form):

    pfs = PortfolioFamily.objects.all()

    name = forms.CharField(max_length=50)
    portfolio_family = forms.ChoiceField(
        choices=[(p.id, p.name) for p in pfs]
    )
