"""
Code for processing uploaded files into system,
e.g. CSV and xlsx files, for either the datamap or database.
"""

import codecs
import csv
import inspect
import re
from importlib import import_module
from typing import Tuple, List

from django import forms
from django.core.files.uploadedfile import UploadedFile

from datamap.models import DatamapLine
from exceptions import IncorrectHeaders


_target_model_exclude = "datamap"


class CSVForm(forms.ModelForm):
    """
    Used to verify an uploaded CSV file, line-by-line.
    """

    class Meta:
        model = DatamapLine
        exclude = [_target_model_exclude]  # this is the ForeignKey


def _validate_dmlines_from_csv(csv_file: UploadedFile) -> Tuple[int, List[dict]]:
    """
    Use a Form to validate input in an uploaded CSV
    file.
    :param csv_file: an opened file object
    :return: tuple of records added and errors
    """

    _id_regex = re.compile(".*_id$", re.I)

    records_added = 0
    errors = []

    csv_reader = csv.DictReader(codecs.iterdecode(csv_file, "utf-8"))
    for row in csv_reader:
        form = CSVForm(row)
        if form.is_valid():
            # process
            records_added += 1
        else:
            try:
                for k in form.errors.keys():
                    print(
                        f"Error in {k}: {form.data[k]}\n" f"Detail: {form.errors[k][0]}"
                    )
                errors.append(form.errors)
            except KeyError:
                # introspect models.py to get correct expected csv headers
                # and send with this exception

                _models = import_module(f"{_target_model_exclude}.models")
                _model_classes = [
                    (k, v) for k, v in inspect.getmembers(_models) if inspect.isclass(v)
                ]
                _keys = [
                    name
                    for name in _model_classes[1][1].__dict__.keys()
                    if name not in [
                        "id",
                        "__module__",
                        "__doc__",
                        "_meta",
                        "DoesNotExist",
                        "MultipleObjectsReturned",
                        "objects",
                        "__str__",
                    ]
                ]
                _keys = [k for k in _keys if not re.match(_id_regex, k)]
                _keys = [k for k in _keys if k != _target_model_exclude]

                raise IncorrectHeaders(
                    f"Incorrect headers in csv file - should be: {','.join(_keys)}"
                )
    return records_added, errors
