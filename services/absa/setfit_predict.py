from services.absa.load_model import LoadModel

def predict_data(text):
    preds = LoadModel()

    return list(preds.model(text))