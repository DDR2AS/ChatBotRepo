import pickle
import json
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from chatbot import *
from quickstart import *

global service
def main():
    #Para el chatbot
    lemmatizer = WordNetLemmatizer()
    intents = json.loads(open("intents.json").read())

    words = pickle.load(open("words.pkl", "rb"))
    classes = pickle.load(open("classes.pkl", "rb"))
    model = load_model("chatbotmodel.h5")
    service = setupGoogleCalendar();

    result = service.calendarList().list().execute()
    print(result['items'][2])


    print("GO! Bot is running!")
    print("Bienvenido al servicio de Doc Neuralito\n")
    while True:
        message = input("")
        ints = predict_class(message)
        res = get_response(ints, intents)
        print(res)



if __name__ == "__main__":
    main()
