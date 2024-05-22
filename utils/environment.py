from dotenv import load_dotenv
import os
from pathlib import Path

def load_env():
    STAGE = os.getenv("STAGE","DEV")
    BASE_DIR = os.path.join(os.path.dirname(__file__), '../')

    if STAGE == "PROD":
        load_dotenv(BASE_DIR+".prod.env")

    elif STAGE == "DEV":
        load_dotenv(BASE_DIR+".dev.env")

    elif STAGE == "STAGING":
        load_dotenv(BASE_DIR+".stage.env")

        
def get_env(key,coal=False):
    return os.environ.get(key,coal) if coal else os.environ.get(key)

def load_env_settings():
    STAGE = os.getenv("STAGE","DEV")

    if STAGE == "PROD":
        return "absa.settings.production"

    elif STAGE == "DEV":
        return "absa.settings.development"

    elif STAGE == "STAGING":
        return "absa.settings.staging"