import csv
import tempfile

from io import StringIO

import pytest


TEMPDIR = tempfile.gettempdir()


@pytest.fixture
def uploaded_csv_file():
    uf = StringIO()
    uf.write("key,sheet,cell_ref\n")
    uf.write("First row col 1,First row col 2,A15\n")
    uf.write("Second row col 1,Second row col 2,B15\n")
    uf.write("Third row col 1,Third row col 2,C15\n")
    uf.write("Fourth row col 1,Fourth row col 2,D15\n")
    yield uf
    uf.close()


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
