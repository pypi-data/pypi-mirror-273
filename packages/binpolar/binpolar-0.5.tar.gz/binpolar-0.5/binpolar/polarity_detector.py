import re
import tensorflow as tf
from transformers import DistilBertTokenizer

# Define global variables for the model and tokenizer
_model = None
_tokenizer = None

# Lazily loads and returns the model and tokenizer
def get_model():
    global _model
    if _model is None:
        _model = tf.keras.models.load_model('ocean_isPos')
    return _model

def get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = DistilBertTokenizer.from_pretrained('ocean_isPos/tokenizer')
    return _tokenizer

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text).lower()
    return text

def detect_polarity(input):
    # 1 is positive 0 is negative
    model = get_model()
    tokenizer = get_tokenizer()

    text = preprocess_text(input)
    sentiment_en = tokenizer(text, truncation=True, padding=True, return_tensors='tf')
    s_input_ids = sentiment_en['input_ids']
    s_attention_mask = sentiment_en['attention_mask']
    s_output = model.predict({'input_ids': s_input_ids, 'attention_mask': s_attention_mask})

    prob = s_output[0]
    print("pos_probabilities:", prob)
    isPos = (prob > 0.5).astype(int)

    return isPos