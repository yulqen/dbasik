import pytest
import tempfile

TEMPDIR = tempfile.gettempdir()


@pytest.fixture
def uploaded_csv_file():
    uf = "/".join([TEMPDIR, 'datamap.csv'])
    with open(uf, 'w') as f:
        f.write("First line")
        f.write("Second line")
    return uf
