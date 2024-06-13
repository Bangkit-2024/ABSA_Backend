from google.cloud import translate_v2 as translate


def translate_text_to_languages(text, target_language:str='id',simple:bool=False)->dict|str:
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    
    if simple:
        return result["translatedText"]
    
    return {
            "translatedText": result["translatedText"],
            "detectedSourceLanguage": result["detectedSourceLanguage"]
        }