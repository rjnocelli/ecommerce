from .base import *

DEBUG = False

DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'dulceria',
    'USER': 'rjnocelli',
    'PASSWORD': '4K6j0clhi',
    'HOST': '192.241.137.29',
    'PORT': '',
    }
}

ALLOWED_HOSTS = ['192.241.137.29']

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True