import os

from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(pathname)s %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "datamap_console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "returns_console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 5,
            "filename": f"{BASE_DIR}/logs/dbasik.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {"handlers": ["file", "console"], "level": "INFO", "propagate": True},
        "datamap.views": {
            "handlers": ["file", "datamap_console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "returns.views": {
            "handlers": ["file", "returns_console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

INSTALLED_APPS.append("django_extensions")
INSTALLED_APPS.append("behave_django")

ALLOWED_HOSTS.append("localhost")

CRISPY_FAIL_SILENTLY = not DEBUG

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "HOST": "localhost",
#         "NAME": "db.sqlite3",
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbasik',
        'USER': 'dbasikuser',
        'PASSWORD': 'dbasik',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
