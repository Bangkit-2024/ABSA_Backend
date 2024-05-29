from absa.settings.common import *
from utils.environment import load_env, get_env
import os

SECRET_KEY = os.environ.get("DJANGO_SECRET")
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USERNAME"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST':os.environ.get("DB_HOST"),
        'PORT':'3306',
    }
}