"""
Django settings for informer project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os, environ
from pathlib import Path
from django.conf import settings as default_settings


env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-f71wevx&=04*+4@96a1ltskmaj2)%w^%$gl1@_)gyzi)50epas')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK' :  lambda request: default_settings.DEBUG or request.GET.get('iddqd', False)
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost'])

SECURE_SSL_REDIRECT = False
# Application definition

INSTALLED_APPS = [
    'informer.apps.InformerAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_bootstrap5',
    'hijack',
    'hijack.contrib.admin',
    'rest_framework',
    'django_dramatiq',
    'accounts.apps.AccountsConfig',
    'flows.apps.FlowsConfig',
    'contacts.apps.ContactsConfig',
    'inbox.apps.InboxConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'accounts.middleware.CheckSiteMiddleware',
    'hijack.middleware.HijackUserMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'informer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ 'informer/templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'informer.context_processors.rollbar_settings'
            ],
        },
    },
]

WSGI_APPLICATION = 'informer.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///%s' % os.path.join(BASE_DIR, 'db.sqlite3'))
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


from django.http import Http404
from django.core.exceptions import PermissionDenied

ROLLBAR_CLIENT_TOKEN = env('ROLLBAR_CLIENT_TOKEN', default='')

ROLLBAR = {
    'access_token': env('ROLLBAR_TOKEN', default=''),
    'environment': env('ROLLBAR_ENVIRONMENT', default='development'),
    'root': BASE_DIR,
    'code_version': '1.0',
    'exception_level_filters': [
        (Http404, 'ignored'),
        (PermissionDenied, 'ignored'),
    ],
}


LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'rollbar': {
            'access_token': env('ROLLBAR_TOKEN', default=''),
            'environment': 'development' if DEBUG else 'production',
            'class': 'rollbar.logger.RollbarHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': ['rollbar', 'console'],
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
        },
    },
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rollbar.contrib.django_rest_framework.post_exception_handler'
}

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'accounts:environment_list'
LOGOUT_REDIRECT_URL = 'home'

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {
        "url": env.str("DRAMATIQ_REDIS_URL"),
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ]
}

DRAMATIQ_AUTODISCOVER_MODULES = ["executors.dramatiq_executor"]


if env.str("CONTACT_STORAGE", default=False):
    CONTACT_STORAGE = env.str("CONTACT_STORAGE")


if env.str("INBOX_ENTRY_STORAGE", default=False):
    INBOX_ENTRY_STORAGE = env.str("INBOX_ENTRY_STORAGE")
