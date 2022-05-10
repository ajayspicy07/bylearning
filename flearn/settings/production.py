

''' PRODUCTION SETTINGS '''

from flearn.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['www.bylearning.in', 'bylearning.in', 'ip address']

#
DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'postgres',

        'USER': 'bylearner',

        'PASSWORD': '',

        'HOST': '',

        'PORT': '5432',

    }

}



#EMAIL BACKEND
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST   = 'smtp.gmail.com'
EMAIL_PORT  = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bylearning.official@gmail.com'
EMAIL_HOST_PASSWORD = ' '








#S3 BUCKET SETTINGS HAVE TO MAINTAIN IN SECRET
AWS_ACCESS_KEY_ID = ' '
AWS_SECRET_ACCESS_KEY = ' '
AWS_STORAGE_BUCKET_NAME = 'bylearning-media-files'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
DEFAULT_FILE_STORAGE = 'flearn.settings.storage_backends.MediaStorage'


