import pytest


@pytest.fixture(scope='session')
def django_db_setup():
    from django.conf import settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'dbasik_dftgovernance',
        'USER': 'lemon',
        'PORT': '5432',
        'PASSWORD': 'lemon'
    }
