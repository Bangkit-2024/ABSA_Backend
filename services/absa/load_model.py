from setfit import AbsaModel

class LoadModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoadModel, cls).__new__(cls)
            cls._instance.model = AbsaModel.from_pretrained(
    "services/absa/model/absa_model_test-aspect",
    "services/absa/model/absa_model_test-polarity",
    )
        return cls._instance

