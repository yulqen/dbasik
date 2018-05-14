from io import StringIO, BytesIO

import pytest

from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'fixtures/data.json')


#@pytest.fixture(scope='session')
#def django_db_setup():
#    from django.conf import settings
#    settings.DATABASES['default'] = {
#        'ENGINE': 'django.db.backends.postgresql',
#        'HOST': 'localhost',
#        'NAME': 'dbasik_dftgovernance',
#        'USER': 'lemon',
#        'PORT': '5432',
#        'PASSWORD': 'lemon'
#    }


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
def bad_csv_file(tmpdir):
    uf = tmpdir.mkdir("csv-files").join('bad_datamap.csv')
    with open(uf, 'w') as f:
        f.write("bad_key,bad_sheet,bad_cell_ref\n")
        f.write("First row col 1,First row col 2,A15\n")
        f.write("Second row col 1,Second row col 2,B15\n")
        f.write("Third row col 1,Third row col 2,C15\n")
        f.write("Fourth row col 1,Fourth row col 2,D15\n")
    return uf.strpath


@pytest.fixture
def csv_hundred_plus_key(tmpdir):
    uf = tmpdir.mkdir("csv-files").join('big_key_csv.csv')
    k = ("This is a key that is way too long and need to be "
         "seriously truncated we dont like keys this length do we?")
    with open(uf, 'w') as f:
        f.write("key,sheet,cell_ref\n")
        f.write(f"{k},First row col 2,A15\n")
        f.write("Second row col 1,Second row col 2,B15\n")
        f.write("Third row col 1,Third row col 2,C15\n")
        f.write("Fourth row col 1,Fourth row col 2,D15\n")
    return uf.strpath



@pytest.fixture
def good_csv_file(tmpdir):
    uf = tmpdir.mkdir("csv-files").join('good_datamap.csv')
    with open(uf, 'w') as f:
        f.write("key,sheet,cell_ref\n")
        f.write("First row col 1,First row col 2,A15\n")
        f.write("Second row col 1,Second row col 2,B15\n")
        f.write("Third row col 1,Third row col 2,C15\n")
        f.write("Fourth row col 1,Fourth row col 2,D15\n")
    return uf.strpath


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
