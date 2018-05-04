"""
Code for processing uploaded files into system,
e.g. CSV and xlsx files, for either the datamap or database.
"""

from django import forms

from datamap.models import DatamapLine


class CSVForm(forms.ModelForm):

    class Meta:
        model = DatamapLine
