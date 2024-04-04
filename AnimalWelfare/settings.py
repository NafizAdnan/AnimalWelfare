
from pathlib import Path
from . info import *

EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = EMAIL_HOST
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_PORT = EMAIL_PORT
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0qb+8@b#k7i=(l6)hkhu!c$$+9ng%4418kzgvmsfr51br11css'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'baseapp',
    'channels',
    'notification_app',
    'django_celery_results',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',


]

ROOT_URLCONF = 'AnimalWelfare.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'baseapp/templates',
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'baseapp.custom_context_processors.notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'AnimalWelfare.wsgi.application'
ASGI_APPLICATION = 'AnimalWelfare.asgi.application'

# CHANNEL_LAYERS = {
#     'default' : {
#         'BACKEND' : 'channels.layers.InMemoryChannelLayer'

    
        
#     }

# }

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}



# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'baseapp.User'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'assets/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
import os
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# STATIC_ROOT = BASE_DIR / 'static'

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')  # ! Static Directory

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'baseapp/assets')  # ! Static Files Directory

]  # ! Static Files Directory

INTERNAL_IPS = [
    "*",
    '127.0.0.1'
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
IMAGGA_API_KEY = 'acc_2c50c2a33049d25'
IMAGGA_API_SECRET = 'c6cfd170d8b52a7c77196649bb5895dd'
IMAGGA_API_AUTH_HEADER = 'Basic YWNjXzJjNTBjMmEzMzA0OWQyNTpjNmNmZDE3MGQ4YjUyYTdjNzcxOTY2NDliYjU4OTVkZA=='
TEMP_UPLOAD_DIR = os.path.join(MEDIA_ROOT, 'temp_uploads')

# CELERY SETTINGS

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Dhaka'
CELERY_RESULT_BACKEND = 'django-db'

#CELERY BEAT

CELERY_BEAT_SCEDULER = 'django_celery_beat.schedulers:DatabseScheduler'