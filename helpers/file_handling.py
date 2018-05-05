from django.core.files.uploadedfile import UploadedFile

from helpers.file_processors import add_datamaplines_from_csv
from exceptions import IllegalFileUpload


class CleanUploadedFile:

    """Once a file has been uploaded, this handler is called
    to sort out it's file type and pass on to the appropriate
    processor. If the filetype is not in UploadedFileHandler.accessible_types
    an IllegalFileUpload exception is raised."""

    acceptable_types = {
        'csv': ['text/csv'],
        'xlsx': ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
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
        vals = self.acceptable_types.values()
        hit = 0
        for v in vals:
            for x in v:
                if self._content_type == x:
                    hit += 1
        if hit == 0:
            raise IllegalFileUpload
        else:
            for i in self.acceptable_types.keys():
                for x in self.acceptable_types[i]:
                    if x == self._content_type:
                        self._short_type = i
                        self._acceptable_type = True
                        return

        # if there are no lists that form values in the accessible_types dict,
        # we can just test for the filetpe in the accessible_type dict's
        # values as normal, and raise an exception if not found

        # HERE WE CAN PLUG IN OTHER FILE CHECKING CODE IF WE NEED IT
        # e.g. check for OpenOfficeXML (xlsx) format by attempting
        # and unzip and inspect bytes, or by checking for csv semantics

        # else:
        #   if not XlsxTest(self_uploaded_file).pass:
        #       raise IllegalFileUpload
        # if we get to this poit, no exception has been raised, therefore
        # the filetype is acceptible.


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
        # FOR THE CSV HANDLING, WE USE FORMS AS SET OUT IN p164 of TWO SCOOPS
        print(f"We are now in the UploadedFileHandler.process() method "
              f"with {self._f} which is a {self._acceptable_type}")
        print(f"Passing the file to add_datamap_lines_from_csv")
        if self._short_type == 'csv':
            res = add_datamaplines_from_csv(self._f)
            print(res)
        else:
            print("NOT A CSV!")

