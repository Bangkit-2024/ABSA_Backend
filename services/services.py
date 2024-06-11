from services.gcloud.cloud_translation import translate_text_to_languages as gcloud_translate
from services.free.libre_translate import translate_text_to_languages as free_translate
from services.absa.load_model import LoadAbsaModel, LoadLSTMModel

def translate_services(text:str,target:str='id')->str:
    """Translate your text to Bahasa Indonesia

    I've separated services that connect to the 3rd party
    from this function in case if someone want to change 
    the api that they are use.

    But remember it shoud have args text and target language
    And it only return string

    Args:
        text (str): Text that will be translated

    Returns:
        str: Translation result
    """

    # This is for google translate API
    # We also provide another API services in 'free' section if you want to use
    try:
        return gcloud_translate(text,target, simple=True)
    except:
        return free_translate(text,target)

def predict_services(text):

    absa_model = LoadAbsaModel() 
    ltsm_model = LoadLSTMModel()
    
    setfit_result = absa_model.model(text)
    lstm_result = ltsm_model.predict(text,setfit_result)
    print(setfit_result)
    print(lstm_result)

    return {"span":setfit_result,"absa":lstm_result}
    