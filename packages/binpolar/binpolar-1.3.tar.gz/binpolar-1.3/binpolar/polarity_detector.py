import re
import os
# import tensorflow as tf
from transformers import DistilBertTokenizer
from huggingface_hub import from_pretrained_keras

model = from_pretrained_keras("joycerlz/distilbert-binary-polar")

path = os.path.dirname(__file__)
tokenizer = DistilBertTokenizer.from_pretrained(path + '/tokenizer')

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text).lower()
    return text

def detect_polarity(input):
    # 1 is positive 0 is negative
    text = preprocess_text(input)
    sentiment_en = tokenizer(text, truncation=True, padding=True, return_tensors='tf')
    s_input_ids = sentiment_en['input_ids']
    s_attention_mask = sentiment_en['attention_mask']
    s_output = model.predict({'input_ids': s_input_ids, 'attention_mask': s_attention_mask})

    prob = s_output[0]
    isPos = (prob > 0.5).astype(int)
    print("Predicted probability:", prob[0])
    if isPos:
        print('Predicted positive.')
    else:
        print('Predicted negative')

    return isPos