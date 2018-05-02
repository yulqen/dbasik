import csv

from django.test import TestCase
from django.core.files.uploadedfile import UploadedFile


def test_uploaded_file(uploaded_csv_file):
    test_file = open(uploaded_csv_file)
    uf = UploadedFile(test_file)
    assert uf.name == 'datamap.csv'


def test_csv_contents(uploaded_csv_file):
    test_file = open(uploaded_csv_file)
    uf = UploadedFile(test_file)
    csv_reader = csv.DictReader(uf)
    line = next(csv_reader)
    assert line['header_1'] == 'First row col 1'
    assert line['header_2'] == 'First row col 2'
    assert line['header_3'] == 'First row col 3'
    line = next(csv_reader)
    assert line['header_1'] == 'Second row col 1'
    assert line['header_2'] == 'Second row col 2'
    assert line['header_3'] == 'Second row col 3'
