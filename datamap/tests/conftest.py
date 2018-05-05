import csv
import tempfile

import pytest


TEMPDIR = tempfile.gettempdir()


@pytest.fixture
def uploaded_csv_file():
    uf = "/".join([TEMPDIR, 'datamap.csv'])
    with open(uf, 'w') as f:
        fieldnames = ['key', 'sheet', 'cell_ref']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'key': "First row col 1", 'sheet': 'First row col 2', 'cell_ref': 'A15'})
        writer.writerow({'key': "Second row col 1", 'sheet': 'Second row col 2', 'cell_ref': 'B15'})
        writer.writerow({'key': "Third row col 1", 'sheet': 'Third row col 2', 'cell_ref': 'C15'})
    return uf


@pytest.fixture
def uploaded_csv_file_bytes():
    uf = "/".join([TEMPDIR, 'datamap.csv'])
    with open(uf, 'w') as f:
        fieldnames = ['key', 'sheet', 'cell_ref']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'key': "First row col 1", 'sheet': 'First row col 2', 'cell_ref': 'A15'})
        writer.writerow({'key': "Second row col 1", 'sheet': 'Second row col 2', 'cell_ref': 'B15'})
        writer.writerow({'key': "Third row col 1", 'sheet': 'Third row col 2', 'cell_ref': 'C15'})
    return open(uf, 'r+b')
