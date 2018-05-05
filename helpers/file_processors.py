"""
Code for processing uploaded files into system,
e.g. CSV and xlsx files, for either the datamap or database.
"""

import csv
import codecs

from django import forms

from datamap.models import DatamapLine


class CSVForm(forms.ModelForm):
    """
    Used to verify an uploaded CSV file, line-by-line.
    """

    class Meta:
        model = DatamapLine
        exclude = ['datamap'] # this is the ForeignKey


def add_datamaplines_from_csv(csv_file):
    """
    Use a Form to validate input in an uploaded CSV
    file.
    :param csv_file: an opened file object
    :return: tuple of records added and errors
    """

    records_added = 0
    errors = []

    csv_reader = csv.DictReader(codecs.iterdecode(csv_file, 'utf-8'))
    for row in csv_reader:
        form = CSVForm(row)
        if form.is_valid():
            # process
            records_added += 1
        else:
            errors.append(form.errors)
    return records_added, errors
