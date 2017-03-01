from .settings import *



DEBUG = True


# Don't send emails from staging

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']



