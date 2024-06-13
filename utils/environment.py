from dotenv import load_dotenv
import os
from pathlib import Path
BASE_DIR = os.path.join(os.path.dirname(__file__), '../')


def load_env():
    STAGE = os.getenv("STAGE","DEV")

    if STAGE == "PROD":
        load_dotenv(BASE_DIR+".prod.env")

    elif STAGE == "DEV":
        load_dotenv(BASE_DIR+".dev.env")

    elif STAGE == "STAGING":
        load_dotenv(BASE_DIR+".stage.env")

        
def get_env(key,coal=False):
    return os.environ.get(key,coal) if coal else os.environ.get(key)

def load_gcloud_env():

    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = BASE_DIR+'credentials.json'

def load_env_settings():
    STAGE = os.getenv("STAGE","DEV")

    if STAGE == "PROD":
        return "absa.settings.production"

    elif STAGE == "DEV":
        return "absa.settings.development"

    elif STAGE == "STAGING":
        return "absa.settings.staging"