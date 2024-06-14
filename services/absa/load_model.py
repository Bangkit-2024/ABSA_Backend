from setfit import AbsaModel
from services.absa.ltsm_predict import LSTMModel
from services.absa.preprocess import PreprocessData
from django.conf import settings
from utils.STATICVAR import APP_DIR


class Singleton(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

# We Save this for later
class LoadAbsaModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoadAbsaModel, cls).__new__(cls)
            cls._instance.model = AbsaModel.from_pretrained(
        APP_DIR+"services/absa/model/large_model/absa-aspect",
        APP_DIR+"services/absa/model/large_model/absa-polarity",
    spacy_model="id_core_news_trf"
    )
        return cls._instance
       
class LoadLSTMModel(metaclass=Singleton):

    def __init__(self):
        self.model = LSTMModel()
        
    def predict(self,text,preds):
        return self.model.predict_text(text,[preds])

class Preprocess(metaclass=Singleton):

    def __init__(self):
        self.model = PreprocessData()
        
    def preprocess(self,text):
        return self.model.preprocess_text(text)

    