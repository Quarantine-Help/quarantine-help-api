# SECURITY WARNING: keep the secret key used in production secret!
import os

from quarantined_backend.settings import BASE_DIR

SECRET_KEY = "%5r@$^)+$$#$%ˆˆ%ˆˆˆˆ%$%%$&ˆˆFFDFDSFSDF@$@#DSSFDZzzzSAe3n%fm_"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# We do not support sqlite anymore
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "DATABASE_NAME",
        "USER": "DATABASE_USER",
        "PASSWORD": "DATABASE_PASSWORD",
        "HOST": "DATABASE_HOST",
        "PORT": "",
    }
}
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Add datetime string format to the API responses
REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%S%z"
}

ALLOWED_HOSTS = []

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="sentrydsn",
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
