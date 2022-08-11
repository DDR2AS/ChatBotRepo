import random
import json
import pickle
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Activation,Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer
intents = json.loads(open('intents.json').read()) #Creación de diccionario

#Creamos 3 listas vacias
words = []
classes = []
documents = []
ignore_letters = ['?','!','.',',']

#Ahora necesitamos acceder al objeto intents y a los keys y a los diccionarios internos
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern) #Al recibir una cadena de caracteres, se dividen en una lista de palabras individuales en una collección
        words.append(word_list)
        documents.append((word_list,intent['tag'])) #Pasamos una tupla
        #Luego verificamos si la clase se encuentra en nuestra lista de clases
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

print(documents)
