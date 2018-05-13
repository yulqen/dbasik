import csv

from django.core.files.uploadedfile import UploadedFile


def test_good_csv_file(good_csv_file):
    with open(good_csv_file, 'r') as f:
        uf = UploadedFile(f)
        csv_reader = csv.DictReader(uf)
        line = next(csv_reader)
        assert line["key"] == "First row col 1"
        assert line["sheet"] == "First row col 2"
        assert line["cell_ref"] == "A15"
        line = next(csv_reader)
        assert line["key"] == "Second row col 1"
        assert line["sheet"] == "Second row col 2"
        assert line["cell_ref"] == "B15"


def test_csv_contents(uploaded_csv_file):
    uf = UploadedFile(uploaded_csv_file)
    csv_reader = csv.DictReader(uf)
    line = next(csv_reader)
    assert line["key"] == "First row col 1"
    assert line["sheet"] == "First row col 2"
    assert line["cell_ref"] == "A15"
    line = next(csv_reader)
    assert line["key"] == "Second row col 1"
    assert line["sheet"] == "Second row col 2"
    assert line["cell_ref"] == "B15"
