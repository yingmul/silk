from settings.common import *

DEBUG=False
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
    'storages', #django-storages
)

from os import environ
from urlparse import urlparse

if environ.has_key('DATABASE_URL'):
    url = urlparse(environ['DATABASE_URL'])
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
    }

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
COMPRESS_PRECOMPILERS = (('text/less', "lessc '{infile}' '{outfile}'"),)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# serving static files from heroku https://devcenter.heroku.com/articles/django-assets
import os
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
# MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media'),
#
# # URL that handles the media served from MEDIA_ROOT. Make sure to use a
# # trailing slash.
# # Examples: "http://example.com/media/", "http://media.example.com/"
# MEDIA_URL = '/media/'


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'stylieu-assets'
# STATIC_URL = '//s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
# ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
MEDIA_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

