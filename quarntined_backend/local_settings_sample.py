# SECURITY WARNING: keep the secret key used in production secret!
import os

from quarntined_backend.settings import BASE_DIR

SECRET_KEY = "%5r@$^)+$$#$%ˆˆ%ˆˆˆˆ%$%%$&ˆˆFFDFDSFSDF@$@#DSSFDZzzzSAe3n%fm_"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

ALLOWED_HOSTS = []
