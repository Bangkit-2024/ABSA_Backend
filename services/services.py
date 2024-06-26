from services.gcloud.cloud_translation import translate_text_to_languages as gcloud_translate
from services.free.libre_translate import translate_text_to_languages as free_translate
from services.absa.load_model import LoadAbsaModel, LoadLSTMModel, Preprocess as PreprocessData

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

def sentiment_output_converter(sentiment:str)->int:

    if(sentiment=="positif"):
        return 1
    
    if(sentiment=="negatif"):
        return -1
    
    return 0
        

def predict_services(text):
    
    print("Predict ",text)
    preprocess = PreprocessData()
    absa_model = LoadAbsaModel() 
    ltsm_model = LoadLSTMModel()
    
    process_text = preprocess.preprocess(text)
    setfit_result = absa_model.model(process_text)
    lstm_result = [[]]
    if len(setfit_result[0]) :
        lstm_result = ltsm_model.predict(process_text,setfit_result)
        


    return {"span":setfit_result,"absa":lstm_result}