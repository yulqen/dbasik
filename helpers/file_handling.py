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


# used in introspecting the model for datamap class
# TODO this should come from the config and might not
# even be needed at all. Check the CSVFileUpload class

target_model_exclude = "datamap"

acceptable_types = {
    "csv": ["text/csv"],
    "xlsx": ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
    "xlsm": [
        "application/vnd.ms-excel.sheet.macroEnabled.12",
        "application/vnd.ms-excel.sheet.macroenabled.12",
    ],
}


class CSVForm(forms.ModelForm):
    """
    Used to verify an uploaded CSV file, line-by-line.
    """

    class Meta:
        model = DatamapLine
        exclude = [target_model_exclude]  # this is the ForeignKey


class DBUploadedFile:
    """Base class for files uploaded to the the dbasik system.

    Not to be implemented directly.
    """

    def __init__(self, uploaded_file: UploadedFile) -> None:
        """Initialise with an opened file object and its short type.
        """
        self._uploaded_file = uploaded_file

    def process(self):
        raise NotImplementedError()


class CSVUploadedFile(DBUploadedFile):
    """Handles uploaded CSV files.
    """

    def _validate_dmlines_from_csv(
        self, csv_file: UploadedFile
    ) -> Tuple[int, List[dict]]:
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
                            f"Error in {k}: {form.data[k]}\n"
                            f"Detail: {form.errors[k][0]}"
                        )
                    errors.append(form.errors)
                except KeyError:
                    # introspect models.py to get correct expected csv headers
                    # and send with this exception

                    _models = import_module(f"{target_model_exclude}.models")
                    _model_classes = [
                        (k, v)
                        for k, v in inspect.getmembers(_models)
                        if inspect.isclass(v)
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
                    _keys = [k for k in _keys if k != target_model_exclude]

                    raise IncorrectHeaders(
                        f"Incorrect headers in csv file - should be: {','.join(_keys)}"
                    )
        return records_added, errors

    def process(self):
        res = self._validate_dmlines_from_csv(self._uploaded_file)
        print(res)


class XLSXUploadedFile(DBUploadedFile):
    """Handles uploaded Excel files.
    """

    def process(self):
        print(f"Handling an Excel file: {self._uploaded_file}")


class ZipUploadedFile(DBUploadedFile):
    """Handles uploaded zip files.
    """
