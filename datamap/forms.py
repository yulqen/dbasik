from django import forms
from .models import PortfolioFamily


class CreateDatamapForm(forms.Form):

    pfs = PortfolioFamily.objects.all()

    name = forms.CharField(max_length=50)
    porfolio_family = forms.ChoiceField(
        choices=[(p.name, p.name) for p in pfs]
    )
