import os

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR = os.path.join(BASE_DIR,'static')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.241.137.29']


INSTALLED_APPS = [
    'inventario_app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'crispy_forms',
    'rest_framework',
    'corsheaders',
    'captcha',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventario.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'inventario.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': os.getenv('SQL_ENGINE', 'sql_engine'),
        'NAME': os.getenv('SQL_NAME', 'sql_name'),
        'USER': os.getenv('SQL_USER', 'sql_user'),
        'PASSWORD': os.getenv('SQL_PASSWORD', 'sql_password'),
        'HOST': os.getenv('SQL_HOST', 'sql_host'),
        'PORT': os.getenv('SQL_PORT', 'sql_port'),
        }
    }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'inventario_app/static/inventario_app'),
]

EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST', 'email_host')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'email_host_user')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'email_host_password')
EMAIL_PORT = 587
PASSWORD_RESET_TIMEOUT_DAYS = 2

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'

PHONENUMBER_DEFAULT_REGION = 'NATIONAL'