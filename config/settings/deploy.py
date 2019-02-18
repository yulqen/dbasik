import os

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

INSTALLED_APPS.append('django_extensions')

ALLOWED_HOSTS = ['209.97.142.1', 'staging.dbasik.com']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# using a specific logging setting for deploy - such as log location
# being at /dbasik/logs/debug.log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'datamap_console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'returns_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5, # 5MB
            'backupCount': 5,
            'filename': f'{BASE_DIR}/logs/dbasik.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'datamap.views': {
            'handlers': ['file', 'datamap_console'],
            'level': 'INFO',
            'propagate': True,
        },
        'returns.views': {
            'handlers': ['file', 'returns_console'],
            'level': 'INFO',
            'propagate': True,
        },
        'excelparser.views': {
            'handlers': ['file', 'returns_console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'excelparser.helpers.parser': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'dbasik_dftgovernance',
        'USER': 'dbasik',
        'PORT': '5432',
        'PASSWORD': 'dbasik'
    }
}
