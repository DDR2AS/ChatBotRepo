import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
# intents = json.loads(open("intents.json").read())

words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))
model = load_model("chatbotmodel.h5")

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
               bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json=json.loads(open("intents.json").read())):
    result = 0
    tag = intents_list[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            if not i["responses"]:
                return "Creo que no te entendi, lo siento"
            result = random.choice(i["responses"])
            break

    return result

print("GO! Bot is running!")

# while True:
#     print("Bienvenido, soy Neuralito y te ayudaré a agendar una cita en el sistema de salud")
#     print("Te pediré unos datos personales para tenerlo todo listo, ¿de acuerdo?")
#
#     while breaker:
#         try:
#             DNI_number = input("Digite su número de DNI: ")
#             c = int(DNI_number)
#             if len(DNI_number) != 8:
#                 raise ZeroDivisionError
#             DNI_number = c
#         except ValueError:
#             print("Por favor ingrese solo números 🤗")
#         except ZeroDivisionError:
#             print("Por favor ingrese un número valido de DNI (tiene 8 dígitos 😉)")
#         else:
#             print("Comprobando DNI en la base de datos. Por favor, espere un momento...")
#             if DNI_probe == DNI_number:
#                 print(f"Gusto en verte {DNI_owner_name}!!!")
#                 breaker = False
#             else:
#                 print("Lo sentimos, el número de DNI ingresado no se encuentra registrado en la RENIEC")
#                 print("Asegurese de estar escribiendo su DNI correcto 😊")
#
#     break

# DNI de corroboración temporal hasta que funcione con la RENIEC
#DNI_probe = 72956984
#DNI_owner_name = "Harold"
#
#a = 0
#flag = True
#
#while True:
#    if a == 0:
#        message = "hola"
#        a += 1
#    else:
#        message = input("*: ")
#    ints = predict_class(message)
#    detected_class = ints[0]["intent"]
#    if detected_class == "citas":
#        res = get_response(ints)
#        print(res)
#        while flag:
#            try:
#                DNI_number = input("Digite su número de DNI: ")
#                c = int(DNI_number)
#                if len(DNI_number) != 8:
#                    raise ZeroDivisionError
#                DNI_number = c
#            except ValueError:
#                print("Por favor ingrese solo números 🤗")
#            except ZeroDivisionError:
#                print("Por favor ingrese un número valido de DNI (tiene 8 dígitos 😉)")
#            else:
#                print("Comprobando DNI en la base de datos. Por favor, espere un momento...")
#                if DNI_probe == DNI_number:
#                    print(f"Gusto en verte {DNI_owner_name}!!!")
#                    flag = False
#                else:
#                    print("Lo sentimos, el número de DNI ingresado no se encuentra registrado en la RENIEC")
#                    print("Asegurese de estar escribiendo su DNI correcto 😊")
#    elif detected_class == "accidentes":
#        res = get_response(ints)
#        print(res)
#        accident_information = input("Ingrese información de lo sucedido: ")
#    elif detected_class == "despedidas":
#        res = get_response(ints)
#        print(res)
#        break
#    else:
#        res = get_response(ints)
#        print(res)



