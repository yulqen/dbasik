from django.test import TestCase
from django.core.files.uploadedfile import UploadedFile


def test_uploaded_file(uploaded_csv_file):
    test_file = open(uploaded_csv_file)
    uf = UploadedFile(test_file)
    assert uf.name == 'datamap.csv'
