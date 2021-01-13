from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': os.getenv('SQL_ENGINE')
        'NAME': os.getenv('SQL_NAME')
        'USER': os.getenv('SQL_USER)
        'PASSWORD': os.getenv('SQL_PASSWORD')
        'HOST': os.getenv('SQL_HOST)
        'PORT': os.getenv('SQL_PORT')
        }
    }

ALLOWED_HOSTS = ['192.241.137.29']

# SECURE_SSL_REDIRECT = True

# SESSION_COOKIE_SECURE = True

# CSRF_COOKIE_SECURE = True

# SECURE_BROWSER_XSS_FILTER = True