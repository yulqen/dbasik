from django.core.files.uploadedfile import UploadedFile

from .generic import splat_listed_dict_values
from exceptions import IllegalFileUpload


class UploadedFileHandler:

    """Once a file has been uploaded, this handler is called
    to sort out it's file type and pass on to the appropriate
    processor. If the filetype is not in UploadedFileHandler.accessible_types
    an IllegalFileUpload exception is raised."""

    acceptible_types = {
        'csv': 'text/csv',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'xlsm': [
            'application/vnd.ms-excel.sheet.macroEnabled.12',
            'application/vnd.ms-excel.sheet.macroenabled.12'
        ]
    }


    def __init__(self, uploaded_file: UploadedFile):
        self._f = uploaded_file
        self._type = uploaded_file.content_type
        self._check_type()

    @property
    def type_being_processed(self):
        return self._type


    def _check_type(self):
        splatted_vals = splat_listed_dict_values(self.acceptible_types.values())
        if splatted_vals:
            if self._type not in splatted_vals:
                raise IllegalFileUpload
        else:
            if self._type not in self.acceptible_types.values():
                raise IllegalFileUpload


    def pass_on(self):
        """TODO: Docstring for pass_on.
        This function creates a processor object depending on the
        filetype of the uploaded file, e.g. a bcompiler process or
        adding the datamap data to the database.

        :returns: TODO
        """
        print(f"We are now in the UploadedFileHandler.pass_on() method "
              f"with {self._f} which is a {self._type}")
