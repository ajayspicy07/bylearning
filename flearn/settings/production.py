

''' PRODUCTION SETTINGS '''

from flearn.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['www.bylearning.in', 'bylearning.in', '148.66.128.241']


DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'postgres',

        'USER': 'bylearner',

        'PASSWORD': 'SpicyAjay07',

        'HOST': 'bylearning.cl450suinxyr.ap-south-1.rds.amazonaws.com',

        'PORT': '5432',

    }

}
