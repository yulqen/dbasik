"""
Code for processing uploaded files into system,
e.g. CSV and xlsx files, for either the datamap or database.
"""

import csv

from django import forms

from datamap.models import DatamapLine


class CSVForm(forms.ModelForm):

    class Meta:
        model = DatamapLine
        exclude = ['datamap']


def add_datamaplines_from_csv(csv_file):

    records_added = 0
    errors = []

    with open(csv_file, 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            form = CSVForm(row)
            if form.is_valid():
                # process
                records_added += 1
            else:
                errors.append(form.errors)
        return records_added, errors
