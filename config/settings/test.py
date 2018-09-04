from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'HOST': 'localhost',
        'NAME': 'test-db.sqlite3',
    }
}
