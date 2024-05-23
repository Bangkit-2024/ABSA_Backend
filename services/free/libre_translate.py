from deep_translator import GoogleTranslator


def translate_text_to_languages(text:str,target:str='id'):
    translated_text = GoogleTranslator('auto',target).translate(text=text)
    return translated_text

print(translate_text_to_languages("Hola amigos, anita maxwiinn my name is xiao","id"))