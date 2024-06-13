from absa.settings.common import *
import os
from utils.environment import load_env, get_env
DEBUG  = True
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

SECRET_KEY = 'django-insecure-4bmcqe^5le)#7^$o22ncyyupozkb)ai+gsj^e5dyx)r=f*1yi%'
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / os.environ.get("DJANGO_DB_NAME"),
    }
}

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append('rest_framework.authentication.SessionAuthentication')
CORS_ALLOW_ALL_ORIGINS=True
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

