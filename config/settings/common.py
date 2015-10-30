# -*- coding: utf-8 -*-
"""
Django settings for wristband project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import sys
import environ
import mongoengine

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path('wristband')

env = environ.Env()

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework_swagger',
    'mongoengine.django.mongo_auth'
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'wristband.apps',
    'wristband.stages',
    'wristband.providers',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'wristband.authentication.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'wristband.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}

# MONGO
# -----------------------------------------------------------------------------

MONGO_DB_NAME = env('MONGO_DB_NAME', default='wristband')
MONGO_USER = env('MONGODB_USER', default='')
MONGO_PASSWORD = env('MONGODB_PASSWORD', default='')
MONGO_HOST = env('MONGODB_HOST', default='localhost')
MONGO_PORT = env('MONGODB_PORT', default='27017')
MONGO_CREDENTIALS = ''

if MONGO_USER and MONGO_PASSWORD:
    MONGO_CREDENTIALS = '{username}:{password}@'.format(username=MONGO_USER,
                                                        password=MONGO_PASSWORD)

MONGO_URI = env('MONGO_URI', default='mongodb://{credentials}{host}:{port}/{db_name}'.format(
    credentials=MONGO_CREDENTIALS,
    host=MONGO_HOST,
    db_name=MONGO_DB_NAME,
    port=MONGO_PORT
))

mongoengine.connect(MONGO_DB_NAME, host=MONGO_URI)

# SESSION
# ------------------------------------------------------------------------------
SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-gb'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOG_LEVEL = env('DJANGO_LOG_LEVEL', default='DEBUG')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'logstash': {
            '()': 'logstash_formatter.LogstashFormatter',
            'format': '{"extra":{"app": "wristband"}}'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'logstash',
            'stream': sys.stdout
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'django.security': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'wristband.authentication': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'wristband.provider': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'wristband.apps.providers': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True
        }
    }
}

# AUTHENTICATION
# -----------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'wristband.authentication.backends.MongoLDAPBackend',
)

AUTH_USER_MODEL = 'mongo_auth.MongoUser'

# REST FRAMEWORK SETTINGS
# ------------------------------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'wristband.authentication.backends.CustomTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# APP SPECIFIC SETTINGS
# -----------------------------------------------------------------------------

STAGES = env('STAGES', default='qa,staging')

PROVIDER_CONFIG = env('PROVIDER_CONFIG', default='providers.yaml')
WEBSTORE_URL = env('WEBSTORE_URL')
KIBANA_URL = env('KIBANA_URL')

