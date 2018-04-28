import os

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

INSTALLED_APPS.append('django_extensions')
INSTALLED_APPS.append('mod_wsgi.server')

STATIC_ROOT = "/vagrant/code/dbasik_dftgovernance/static/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'dbasik_dftgovernance',
        'USER': 'vagrant',
        'PORT': '5432',
        'PASSWORD': 'vagrant'
    }
}
