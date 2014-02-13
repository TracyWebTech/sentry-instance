import os

from sentry.conf.server import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

SENTRY_KEY = os.environ.get('SENTRY_KEY')

SENTRY_URL_PREFIX = 'https://sentry.tracy.com.br'

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = 8000

SENTRY_WEB_OPTIONS = {
    'workers': 3,  # the number of gunicorn workers
    'worker_class': 'gevent',
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
    'certfile': 'ssl/sentry.crt',
    'keyfile': 'ssl/sentry.key',
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SENTRY_CACHE_BACKEND = 'default'

SENTRY_ALLOW_REGISTRATION = False

SOCIAL_AUTH_CREATE_USERS = False
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')
GITHUB_API_SECRET = os.environ.get('GITHUB_API_SECRET')
GITHUB_EXTENDED_PERMISSIONS = ['repo']

DEFAULT_FROM_EMAIL = 'Tracy Logging Service <noreply@tracy.com.br>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER =os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

ALLOWED_HOSTS = ('sentry.tracy.com.br', )
