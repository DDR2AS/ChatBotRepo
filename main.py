import pickle
import json
import nltk
from nltk.stem import WordNetLemmatizer

import time

from tensorflow.keras.models import load_model
from chatbot import *
from quickstart import *

global service

# DNI de corroboración temporal hasta que funcione con la RENIEC
DNI_probe = 72956984
DNI_owner_name = "Harold"


def main():
    # Para el chatbot
    lemmatizer = WordNetLemmatizer()
    intents = json.loads(open("intents.json").read())

    words = pickle.load(open("words.pkl", "rb"))
    classes = pickle.load(open("classes.pkl", "rb"))
    model = load_model("chatbotmodel.h5")

    # service = setupGoogleCalendar();
    # result = service.calendarList().list().execute()
    # print(result['items'][2])

    a = 0
    flag = True

    while True:

        if a == 0:
            message = "hola"
            a += 1
        else:
            message = input("*: ")
        ints = predict_class(message)
        detected_class = ints[0]["intent"]
        if detected_class == "citas":
            res = get_response(ints)
            print(res)
            while flag:
                try:
                    DNI_number = input("Digite su número de DNI: ")
                    c = int(DNI_number)
                    if len(DNI_number) != 8:
                        raise ZeroDivisionError
                    DNI_number = c
                except ValueError:
                    print("Por favor ingrese solo números 🤗")
                except ZeroDivisionError:
                    print("Por favor ingrese un número valido de DNI (tiene 8 dígitos 😉)")
                else:
                    print("Comprobando DNI en la base de datos. Por favor, espere un momento...")
                    # Acá debería ir la conexión con la página de la RENIEC
                    # DNI_owner_name = consult(API_RENIEC(DNI_number))
                    # if DNI_owner_name != "":
                    if DNI_probe == DNI_number:
                        print(f"Gusto en verte {DNI_owner_name}!!!")
                        flag_1 = True
                        hay_cupos = True # Este sirve por ahora para que acepte que si hay cupos
                        while flag_1:
                            print("Necesitaré algunos datos para que agendemos una cita ☺")
                            print("Recuerde que cada una dura de 30 minutos")
                            print(f'Si le es de ayuda la fecha actual es {time.strftime("%d/%m/%y")}')
                            print("Tambien recuerde que solo puede agendar solo una cita por mes y solo hasta un mes "
                                  "después de la fecha actual")
                            Mes = time.strftime("%d/%m/%y")[3:5] # No hay necesidad de preguntar el mes
                            Dia = input("Que dia quiere su cita?: ")
                            # Interaccion con GoogleCalendar para saber si hay cupos
                            print("¿A que hora quiere que sea su cita?")
                            print("Aquí le enseñó horas validas => 10:30:00, 19:00:00, 06:30:00")
                            TiempoInicio_Hora, TiempoInicio_Minuto, TiempoInicio_Segundo = input("Ingrese la fecha en "
                                                                                                 "el siguiente "
                                                                                                 "formato (HH:MM:SS): "
                                                                                                 "").strip().split(":")
                            # Interaccion con GoogleCalendar para saber si hay cupos
                            if hay_cupos:
                                print("Tenemos consultas para el area de cardiologia y consultas generales")
                                print("Recuerde solo ingresar o 'Cardiologia' o 'General'")
                                TipoConsulta = input("¿Que tipo de consulta desea?: ").strip()
                                print("Espere unos instantes mientras se reserva su cita")
                                # Se crea el evento en GoogleCalendar
                                print("La cita fue agendada con éxito!!")
                                message = input("*: ") # Supuestamente, un usuario normal aquí se despediria V:
                                # message = "adios"
                                ints = predict_class(message)
                                res = get_response(ints)
                                print(res)
                                flag = False
                                flag_1 = False
                            else:
                                print("Lo sentimos, no tenemos cupos para la hora deseada")
                    else:
                        print("Lo sentimos, el número de DNI ingresado no se encuentra registrado en la RENIEC")
                        print("Asegurese de estar escribiendo su DNI correcto 😊")

        elif detected_class == "accidentes":
            res = get_response(ints)
            print(res)
            accident_information = input("Ingrese información de lo sucedido: ")
        elif detected_class == "despedidas":
            res = get_response(ints)
            print(res)
            break
        else:
            res = get_response(ints)
            print(res)


if __name__ == "__main__":
    main()
