from tensorflow import keras
from keras.preprocessing.text import Tokenizer
import numpy as np
from keras.models import Sequential
from keras import layers
import tensorflow as tf

from config import modelpath


def create_model():
    maxlen = 100
    from keras.preprocessing.text import Tokenizer
    tokenizer = Tokenizer(num_words=5000)
    vocab_size = len(tokenizer.word_index) + 1
    embedding_dim = 200
    textcnnmodel = Sequential()
    textcnnmodel.add(layers.Embedding(vocab_size, embedding_dim, input_length=maxlen))
    textcnnmodel.add(layers.Conv1D(128, 9, activation='relu'))
    textcnnmodel.add(layers.GlobalMaxPooling1D())
    textcnnmodel.add(layers.Dense(10, activation='relu'))
    textcnnmodel.add(layers.Dense(10, activation='softmax'))
    textcnnmodel.compile(optimizer='adam',
               loss='sparse_categorical_crossentropy',
               metrics=['accuracy'])
    textcnnmodel.summary()
    return textcnnmodel


newmodel = create_model()
newmodel = tf.keras.models.load_model(modelpath)

def predictText(text):

    pad_sequences=keras.preprocessing.sequence.pad_sequences
    textsample=[text]
    tokenizer = Tokenizer(num_words=5000)
    tokenizer.fit_on_texts(textsample)
    Xcnn_sample = tokenizer.texts_to_sequences(textsample)
    maxlen = 100
    Xcnn_sample = pad_sequences(Xcnn_sample, padding='post', maxlen=maxlen)
    prediction=newmodel.predict(np.array(Xcnn_sample))

    print(prediction)
    deptype=["Natural Satement","Study Problems","Peers Problems","Relationship Problems","Loneliness","Hatered","Work Problems","Bored","Unmotivated","Financial Problems"]
    indeks=int(np.where(prediction[0]==np.amax(prediction[0]))[0])
    return  [prediction,indeks,deptype[indeks]]