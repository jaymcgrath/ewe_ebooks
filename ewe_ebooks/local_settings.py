from .settings import *

# Don't send emails from staging

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


