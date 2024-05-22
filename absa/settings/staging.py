from absa.settings.common import *
from utils.environment import load_env, get_env

SECRET_KEY = os.environ.get("DJANGO_SECRET")
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'