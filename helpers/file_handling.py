import codecs
import csv
from typing import NamedTuple
from typing import Tuple, List

from django import forms
from django.core.files.uploadedfile import UploadedFile

from datamap.models import DatamapLine, Datamap
from exceptions import IncorrectHeaders, DatamapLineValidationError


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


class CSVValidationError(NamedTuple):
    """Stores exception data when csv validator throws message.
    We need to pass the data back to the user in a message, so here we go.
    """
    error_field: str
    django_validator_message: str
    field_given_value: str



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
        replace: bool='off'
    ):
        self.model_for_validation = model_for_validation
        self.app_model = app_model
        self.target_dm = target_dm
        self.replace = replace
        self._table_cleared = False
        super().__init__(uploaded_file, given_name)

    def _process(self, row: dict, dm_instance):
        """Save datamap line to database.
        """
        dml = DatamapLine(
            datamap=dm_instance,
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

        records_added = 0
        errors = []

        csv_reader = csv.DictReader(codecs.iterdecode(csv_file, "utf-8"))
        for row in csv_reader:
            form = CSVForm(row)
            if form.is_valid() and self.replace == 'on' and not self._table_cleared:
                dm_inst = Datamap.objects.get(pk=self.target_dm)
                DatamapLine.objects.filter(datamap=dm_inst).delete()
                self._table_cleared = True
                self._process(row, dm_inst)
                records_added += 1
            elif form.is_valid():
                dm_inst = Datamap.objects.get(pk=self.target_dm)
                self._process(row, dm_inst)
                records_added += 1
            else:
                try:
                    for i in form.errors.items():
                        err = CSVValidationError(
                            error_field=i[0],
                            django_validator_message=i[1][0],
                            field_given_value=form.data[i[0]]
                        )
                        errors.append(err)
                except KeyError:
                    _keys = ['key', 'sheet', 'cell_ref']

                    raise IncorrectHeaders(
                        f"Incorrect headers in csv file - should include some "
                        f"of: {','.join(_keys)}"
                    )
        csv_file.close()
        return records_added, errors

    def process(self):
        res = self._validate_dmlines_from_csv(self._uploaded_file)
        try:
            assert res[1] == []
        except AssertionError:
            raise DatamapLineValidationError(res[1])


class XLSXUploadedFile(DBUploadedFile):
    """Handles uploaded Excel files.
    """

    def process(self):
        print(f"Handling an Excel file: {self._uploaded_file}")


class ZipUploadedFile(DBUploadedFile):
    """Handles uploaded zip files.
    """
