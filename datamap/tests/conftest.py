import csv
import tempfile

import pytest


TEMPDIR = tempfile.gettempdir()


@pytest.fixture
def uploaded_csv_file():
    uf = "/".join([TEMPDIR, 'datamap.csv'])
    with open(uf, 'w') as f:
        fieldnames = ['header_1', 'header_2', 'header_3']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'header_1': "First row col 1", 'header_2': 'First row col 2', 'header_3': 'First row col 3'})
        writer.writerow({'header_1': "Second row col 1", 'header_2': 'Second row col 2', 'header_3': 'Second row col 3'})
        writer.writerow({'header_1': "Third row col 1", 'header_2': 'Third row col 2', 'header_3': 'Third row col 3'})
    return uf
