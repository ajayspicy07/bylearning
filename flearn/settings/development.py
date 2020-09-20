
''' Development SETTINGS '''

from flearn.settings.base import *




DEBUG = True

ALLOWED_HOSTS = ['localhost','bylearning.in']

INTERNAL_IPS = ["127.0.0.1", "172.17.0.1"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  'db.sqlite3',
    }
}

#EMAIL SETTINGS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST   = 'smtp.gmail.com'
EMAIL_PORT  = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mr.money2428@gmail.com'
EMAIL_HOST_PASSWORD = 'Ajay@1999'


