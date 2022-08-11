import random
import json
import pickle
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Activation,Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()
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
        words.extend(word_list)
        documents.append((word_list,intent['tag'])) #Pasamos una tupla
        #Luego verificamos si la clase se encuentra en nuestra lista de clases
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open("words.pkl", "wb"))
pickle.dump(words, open("classes.pkl", "wb"))
            
training=[]
output_empty=[0]*len(classes)

for document in documents:
    bag=[]
    word_patterns=document[0]
    word_patterns=[lemmatizer.lemmatize(word.lower())for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag,output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:,0])
train_y = list(training[:,1])

print(training)