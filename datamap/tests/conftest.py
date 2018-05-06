import csv
import tempfile

from io import StringIO, BytesIO

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
    uf.seek(0)
    yield uf
    uf.close()


@pytest.fixture
def uploaded_csv_file_bytes():
    uf = BytesIO()
    uf.write(b"key,sheet,cell_ref\n")
    uf.write(b"First row col 1,First row col 2,A15\n")
    uf.write(b"Second row col 1,Second row col 2,B15\n")
    uf.write(b"Third row col 1,Third row col 2,C15\n")
    uf.write(b"Fourth row col 1,Fourth row col 2,D15\n")
    uf.seek(0)
    yield uf
    uf.close()
