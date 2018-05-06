import csv
import pytest

from exceptions import IllegalFileUpload
from helpers import CSVUploadedFile

from django.core.files.uploadedfile import UploadedFile


#def test_uploaded_file(uploaded_csv_file):
#    uf = UploadedFile(uploaded_csv_file)
#    assert uf.name == 'datamap.csv'


def test_csv_contents(uploaded_csv_file):
    uf = UploadedFile(uploaded_csv_file)
    csv_reader = csv.DictReader(uf)
    line = next(csv_reader)
    assert line['key'] == 'First row col 1'
    assert line['sheet'] == 'First row col 2'
    assert line['cell_ref'] == 'A15'
    line = next(csv_reader)
    assert line['key'] == 'Second row col 1'
    assert line['sheet'] == 'Second row col 2'
    assert line['cell_ref'] == 'B15'

