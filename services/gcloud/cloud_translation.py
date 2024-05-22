# TODO:Letakan Fungsinya dibawah ini
from google.cloud import translate_v2 as translate
import os

# Set environment variable untuk autentikasi
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../gcloud/credentials.json'

# Peta kode bahasa ke nama lengkap bahasa
language_map = {
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "id": "Indo",
    "ar": "Arabic",
    # Tambahkan bahasa lain jika diperlukan
}

def translate_text_to_languages(text, target_languages):
    translate_client = translate.Client()

    translations = {}
    detected_source_language = None
    for language in target_languages:
        result = translate_client.translate(text, target_language=language)
        translations[language] = {
            "translatedText": result["translatedText"],
            "detectedSourceLanguage": result["detectedSourceLanguage"]
        }
        detected_source_language = result["detectedSourceLanguage"]
    
    return translations, detected_source_language

text_to_translate = "你好朋友，这道菜很好吃，这个地方很棒，强烈推荐"
target_languages = ["es", "fr", "de", "id", "ar"]  # Contoh bahasa: Spanyol, Prancis, Jerman, Indo, Arab

translations, detected_source_language = translate_text_to_languages(text_to_translate, target_languages)

# Cetak bahasa sumber yang terdeteksi
source_language_name = language_map.get(detected_source_language, detected_source_language)
print(f'Text: "{text_to_translate}" detected as being in {source_language_name}\n')

# Cetak hasil terjemahan
for language, translation in translations.items():
    target_language_name = language_map.get(language, language)
    print(f'Translated to {target_language_name}: {translation["translatedText"]}\n')
