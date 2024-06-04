from absa.settings.common import *
import os
DEBUG = False
ALLOWED_HOSTS = ['*']
SECRET_KEY = os.environ.get("DJANGO_SECRET")
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'