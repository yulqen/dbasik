from exceptions import IllegalFileUpload

from django.core.files.uploadedfile import UploadedFile


class UploadedFileHandler:

    """Once a file has been uploaded, this handler is called
    to sort out it's file type and pass on to the appropriate
    processor. If the filetype is not in UploadedFileHandler.accessible_types
    an IllegalFileUpload exception is raised."""

    acceptible_types = [
        'text/csv',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel.sheet.macroEnabled.12'
    ]


    def __init__(self, uploaded_file: UploadedFile):
        self._f = uploaded_file
        self._type = uploaded_file.content_type
        self._check_type()

    @property
    def type_being_processed(self):
        return self._type


    def _check_type(self):
        if self._type not in self.acceptible_types:
            raise IllegalFileUpload
        return
