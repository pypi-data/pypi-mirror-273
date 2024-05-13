import tensorflow as tf
from transformers import DistilBertTokenizer
from binpolar.polarity_detector import detect_polarity

# Load the model and tokenizer
model = tf.keras.models.load_model('ocean_isPos')
tokenizer = DistilBertTokenizer.from_pretrained('ocean_isPos/tokenizer')