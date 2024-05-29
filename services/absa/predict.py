import torch
from torch import nn
from transformers import BertTokenizer, AutoModel

# Load the model

# Define the model
class BertForAspectSentimentClassification(nn.Module):
    def __init__(self, bert_model, num_aspect_labels, num_sentiment_labels):
        super(BertForAspectSentimentClassification, self).__init__()
        self.bert = bert_model
        self.aspect_classifier = nn.Linear(bert_model.config.hidden_size, num_aspect_labels)
        self.sentiment_classifier = nn.Linear(bert_model.config.hidden_size, num_sentiment_labels)

    def forward(self, input_ids, attention_mask, aspect_labels=None, sentiment_labels=None):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        sequence_output = outputs.last_hidden_state
        pooled_output = outputs.pooler_output

        aspect_logits = self.aspect_classifier(pooled_output)
        sentiment_logits = self.sentiment_classifier(pooled_output)

        loss = None
        if aspect_labels is not None and sentiment_labels is not None:
            loss_fn = nn.CrossEntropyLoss()
            aspect_loss = loss_fn(aspect_logits, aspect_labels)
            sentiment_loss = loss_fn(sentiment_logits, sentiment_labels)
            loss = aspect_loss + sentiment_loss

        return loss, aspect_logits, sentiment_logits

def predict_aspect(text):
    """Predict the aspect of the given text."""
    model_path = 'services/absa/best_model.pt'
    bert_model = AutoModel.from_pretrained("indolem/indobert-base-uncased")

    model = BertForAspectSentimentClassification(bert_model,4,3)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    tokenizer = BertTokenizer.from_pretrained('services/absa/tokenizer/')

    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_id = torch.argmax(logits, dim=-1).item()
    return predicted_class_id

print(predict_aspect("Hello"))