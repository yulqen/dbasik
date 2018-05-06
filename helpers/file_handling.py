from django.core.files.uploadedfile import UploadedFile

from helpers.file_processors import _validate_dmlines_from_csv
from exceptions import IllegalFileUpload


class DBUploadedFile:
    """Base class for files uploaded to the the dbasik system.

    Not to be implemented directly.
    """

    acceptable_types = {
        'csv': ['text/csv'],
        'xlsx': ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
        'xlsm': [
            'application/vnd.ms-excel.sheet.macroEnabled.12',
            'application/vnd.ms-excel.sheet.macroenabled.12'
        ]
    }

    def __init__(self, uploaded_file):
        """Initialise with an opened file object and its short type.
        """
        self._uploaded_file = uploaded_file
        self.process()

    def process(self):
        raise NotImplementedError()


class CSVUploadedFile(DBUploadedFile):
    """Handles uploaded CSV files.
    """

    def process(self):
        res = _validate_dmlines_from_csv(self._uploaded_file)
        print(res)


class XLSXUploadedFile(DBUploadedFile):
    """Handles uploaded Excel files.
    """

    def process(self):
        print(f"Handling an Excel file: {self._uploaded_file}")


class ZipUploadedFile(DBUploadedFile):
    """Handles uploaded zip files.
    """


