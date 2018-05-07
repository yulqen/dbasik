import codecs
import csv
import inspect
import re
from importlib import import_module
from typing import Tuple, List

from django import forms
from django.core.files.uploadedfile import UploadedFile

from datamap.models import DatamapLine, Datamap
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

    def __init__(self, uploaded_file: UploadedFile, given_name: str) -> None:
        """Initialise with an opened file object and its short type.
        """
        self._uploaded_file = uploaded_file
        self._actual_file_name = self._uploaded_file.name
        self._given_name = given_name

    def process(self):
        raise NotImplementedError()


class CSVUploadedFile(DBUploadedFile):
    """Handles uploaded CSV files.

    :param uploaded_file: an opened file object
    :param model_for_validation: name of model
    :param app_model: name of the Django app in which model object can be found
    :param given_name: name captured by the text box in the HTML form
    """

    def __init__(
        self,
        uploaded_file: UploadedFile,
        model_for_validation: str,
        app_model: str,
        given_name: str,
        target_dm: int,
    ):
        self.model_for_validation = model_for_validation
        self.app_model = app_model
        self.target_dm = target_dm
        super().__init__(uploaded_file, given_name)

    def _process(self, row: dict):
        """Save datamap line to database.
        """
        dm_inst = Datamap.objects.get(pk=self.target_dm)
        dml = DatamapLine(
            datamap=dm_inst,
            key=row['key'],
            sheet=row['sheet'],
            cell_ref=row['cell_ref']
        )
        dml.save()


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
                self._process(row)
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

                    _models = import_module(f"{self.app_model}.models")
                    _model_classes = [
                        (k, v)
                        for k, v in inspect.getmembers(_models)
                        if inspect.isclass(v)
                    ]
                    _target_class = [
                        class_
                        for class_ in _model_classes
                        if class_[0] == self.model_for_validation
                    ]
                    _keys = [
                        name
                        for name in _target_class[0][1].__dict__.keys()
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

                    raise IncorrectHeaders(
                        f"Incorrect headers in csv file - should include some "
                        f"of: {','.join(_keys)}"
                    )
        csv_file.close()
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
