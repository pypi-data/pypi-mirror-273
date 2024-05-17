from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from joblib import load


# Preprocess the input
def preprocess(text): #preprocess in ml-lib
    tokenizer = load('tokenizer.joblib')
    sequences = tokenizer.texts_to_sequences(text)
    padded = pad_sequences(sequences, maxlen=200)
    return padded