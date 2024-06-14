import os

APP_DIR = os.path.join(os.path.dirname(__file__), '../')
SENTIMENT_CODE = {0:"Netral",-1:"Negatif",1:"Positif"}
LANGUAGE_MAP = {
    "es": "Spanish",
    "fr": "French",
    "id": "Indo",
    "en": "English"
    # Tambahkan bahasa lain jika diperlukan
}
PROCESS_TIMEOUT=5
