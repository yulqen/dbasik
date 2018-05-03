from django.core.files.uploadedfile import UploadedFile

from .generic import splat_listed_dict_values
from exceptions import IllegalFileUpload


class CleanUploadedFile:

    """Once a file has been uploaded, this handler is called
    to sort out it's file type and pass on to the appropriate
    processor. If the filetype is not in UploadedFileHandler.accessible_types
    an IllegalFileUpload exception is raised."""

    acceptable_types = {
        'csv': 'text/csv',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'xlsm': [
            'application/vnd.ms-excel.sheet.macroEnabled.12',
            'application/vnd.ms-excel.sheet.macroenabled.12'
        ]
    }


    def __init__(self, uploaded_file: UploadedFile):
        self._f = uploaded_file
        self._content_type = uploaded_file.content_type
        self._acceptable_type = False
        self._check_type()

    @property
    def type_being_processed(self):
        return self._content_type


    def _check_type(self):
        splatted_vals = splat_listed_dict_values(self.acceptable_types.values())
        # if one of the accessible_types dict's values is a list, we test for
        # acceptible values, and raise an exception if not found
        if splatted_vals:
            if self._content_type not in splatted_vals:
                raise IllegalFileUpload
        # if there are no lists that form values in the accessible_types dict,
        # we can just test for the filetpe in the accessible_type dict's
        # values as normal, and raise an exception if not found

        # HERE WE CAN PLUG IN OTHER FILE CHECKING CODE IF WE NEED IT
        # e.g. check for OpenOfficeXML (xlsx) format by attempting
        # and unzip and inspect bytes, or by checking for csv semantics

        # else:
        #   if not XlsxTest(self_uploaded_file).pass:
        #       raise IllegalFileUpload

        else:
            if self._content_type not in self.acceptable_types.values():
                raise IllegalFileUpload
        # if we get to this poit, no exception has been raised, therefore
        # the filetype is acceptible.
        self._acceptable_type = True


    def process(self):
        """TODO: Docstring for process.
        This function creates a processor object depending on the
        filetype of the uploaded file, e.g. a bcompiler process or
        adding the datamap data to the database.

        :returns: TODO
        """
        # another check that the filetype checking process has run
        if self._acceptable_type is not True:
            raise IllegalFileUpload("Cannot call CleanUploadedFile.process() "
                                    "on uninitialised object.")
        # TODO - here we want to perform an action based on the filetype.
        # Reverse engineering the self._acceptable_types dict, when one or
        # any of the values is a list is unnecessarily complex and difficult
        # to come back to, so we need to find another way:
        #   make self._acceptable_types a NamedTuple, with three or four fields
        #   (.e.g key, content-type, content-type-alternate)
        #   get rid of the splatting function and use regex to accept case
        #   insensitive matches when testing the filetype.
        print(f"We are now in the UploadedFileHandler.process() method "
              f"with {self._f} which is a {self._type}")
