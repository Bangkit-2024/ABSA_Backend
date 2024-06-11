from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf

class LSTMModel:
    def __init__(self, model_name='services/absa/model/indobert-base-p1', max_length=128, lstm_model_path='services/absa/model/bilstm_aspect_model.h5'):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.max_length = max_length
        self.lstm_model = tf.keras.models.load_model(lstm_model_path)
        self.label_encoder = LabelEncoder()

        # Set aspect labels and fit the label encoder
        self.aspect_labels = ['harga', 'pelayanan', 'rasa', 'tempat']
        self.label_encoder.fit(self.aspect_labels)

    def get_bert_embeddings(self, span):
        inputs = self.tokenizer(span, return_tensors='pt', truncation=True, padding=True, max_length=self.max_length)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()

    def spans_to_embeddings(self, spans):
        embeddings = []
        for span in spans:
            embedding = self.get_bert_embeddings(span).flatten()
            embeddings.append(embedding)
        return np.array(embeddings)

    def extract_spans(self, preds):
        extracted_spans = []
        for pred in preds:
            if isinstance(pred, list) and all(isinstance(item, dict) for item in pred):
                spans = [item['span'] for item in pred]
            else:
                spans = []
            extracted_spans.append(spans)
        return extracted_spans

    def convert_all_spans_to_embeddings(self, extracted_spans):
        all_embeddings = []
        for spans in extracted_spans:
            if spans:  # Only convert if there are spans
                embeddings = self.spans_to_embeddings(spans)
                all_embeddings.append(embeddings)
            else:
                all_embeddings.append(np.array([]))  # Append empty array if no spans
        return all_embeddings

    def predict_with_lstm(self, embeddings_list):
        if self.lstm_model is None:
            raise ValueError("LSTM model is not loaded.")

        all_embeddings = np.concatenate([embeddings for embeddings in embeddings_list if embeddings.size > 0], axis=0)
        if all_embeddings.size == 0:
            return [[]] * len(embeddings_list)  # Return empty predictions if no embeddings

        all_embeddings = all_embeddings.reshape((all_embeddings.shape[0], 1, all_embeddings.shape[1]))
        preds = self.lstm_model.predict(all_embeddings)
        preds = np.argmax(preds, axis=1)
        aspects = self.label_encoder.inverse_transform(preds)

        predictions = []
        idx = 0
        for embeddings in embeddings_list:
            if embeddings.size > 0:
                predictions.append(aspects[idx : idx + len(embeddings)])
                idx += len(embeddings)
            else:
                predictions.append([])
        return predictions

    def predict_text(self, text, preds):
        """
        Predict the aspects and sentiments for a given text.

        :param text: The input text (string).
        :param preds: The predictions from an aspect extractor (list of dictionaries).
        :return: A list of dictionaries with 'text', 'aspect', and 'sentiment'.
        """
        extracted_spans = self.extract_spans(preds)
        all_embeddings = self.convert_all_spans_to_embeddings(extracted_spans)
        lstm_predictions = self.predict_with_lstm(all_embeddings)
        
        final_predictions = []
        for pred, aspects in zip(preds, lstm_predictions):
            for item, aspect in zip(pred, aspects):
                final_predictions.append({
                    'text': text,
                    'aspect': aspect,
                    'sentiment': item['polarity']
                })
        return final_predictions