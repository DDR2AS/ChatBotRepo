import time
# from tensorflow.keras.models import load_model
from chatbot import *
from quickstart import *
import datefinder

global service
calendarID = 0

def main():
    # Para el chatbot
    # lemmatizer = WordNetLemmatizer()
    # intents = json.loads(open("intents.json").read())
    #
    # words = pickle.load(open("words.pkl", "rb"))
    # classes = pickle.load(open("classes.pkl", "rb"))
    # model = load_model("chatbotmodel.h5")

    CalendarService = setupGoogleCalendar()
    CalendarList = CalendarService.calendarList().list().execute()
    calendar_id = CalendarList['items'][2]['id']

    a = 0
    flag = True
    flag_2 = True

    while flag_2:

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
                    strDNI_number = input("Digite su número de DNI: ")

                    if len(strDNI_number) != 8:
                        raise ZeroDivisionError

                except ValueError:
                    print("Por favor ingrese solo numeros 🤗")

                except ZeroDivisionError:
                    print("Por favor ingrese un numero valido de DNI (tiene 8 digitos 😉)")

                else:
                    print("Comprobando DNI en la base de datos. Por favor, espere un momento...")

                    # Conexión con la página de la RENIEC
                    result = consultNameOwner(strDNI_number)
                    DNI_owner_name = str(result['Names']).strip().lower()
                    DNI_trial = input("Ingrese su nombre (Nombre Apellidos): ").strip().lower()

                    if result['success']:

                        if DNI_trial == DNI_owner_name:

                            print(f"Gusto en verte {DNI_owner_name}!!!")
                            flag_1 = True
                            hay_cupos = True  # Este sirve por ahora para que acepte que si hay cupos (implementar en
                            # la linea 81)

                            while flag_1:
                                print(
                                    "Necesitare algunos datos para que agendemos una cita ☺\nRecuerde que cada una "
                                    "dura 30 minutos")
                                print(f'Si le es de ayuda la fecha actual es {time.strftime("%d/%m/%y")}')
                                print(
                                    "Tambien recuerde que solo puede agendar solo una cita después de la fecha actual ("
                                    "ejem : 13 august 4:30 pm)")

                                # Preguntamos el día y hora de la cita
                                strDateAppointment = input("Indique la fecha y la hora de inicio de la cita: ")

                                # Creación del evento
                                matches = datefinder.find_dates(strDateAppointment)
                                match = list(matches)

                                # Interaccion con GoogleCalendar para saber si hay cupos
                                if len(match):
                                    # Si tenemos una fecha válida encontrada
                                    print(f'La fecha es: {match[0]}')
                                    fecha_valida = True

                                else:
                                    print("Fecha invalida")
                                    fecha_valida = False

                                # Interacción con GoogleCalendar para saber si hay cupos
                                if hay_cupos & fecha_valida:
                                    print("Tenemos consultas para el area de cardiologia y consultas "
                                          "generales\nRecuerde solo ingresar o 'Cardiologia' o 'General'")
                                    TipoConsulta = input("¿Que tipo de consulta desea?: ").strip()
                                    print("Espere unos instantes mientras se reserva su cita")

                                    # Creación de la descripción
                                    description = "Hospital EsSalud\n" + "Paciente: " + DNI_owner_name

                                    # Se crea el evento en GoogleCalendar
                                    eventbody = CreateEvent(calendar_id, CalendarService, strDateAppointment,
                                                            TipoConsulta, description)

                                    if eventbody is not None:
                                        print(f"La cita fue agendada con éxito para el {match}!!\n {eventbody}")

                                    else:
                                        print("Lo sentimos, la cita no pudo ser agendada")

                                    print("¿Puedo hacer algo mas por ti?")
                                    message = input("*: ")  # Supuestamente, un usuario normal aquí se despediria V:
                                    # message = "adios"
                                    ints = predict_class(message)
                                    res = get_response(ints)
                                    print(res)

                                    flag = False
                                    flag_1 = False
                                    flag_2 = False

                                else:
                                    print("Lo sentimos, no tenemos cupos para la hora deseada")

                        else:
                            print("No pudimos verificar tus datos")

                    else:
                        print("Lo sentimos, el número de DNI ingresado no se encuentra registrado en la RENIEC")
                        print("Asegurese de estar escribiendo su DNI correctamente 😊")

        elif detected_class == "accidentes":
            res = get_response(ints)
            print(res)
            accident_information = input("Ingrese informacion de lo sucedido: ")
            print("Nos comunicaremos contigo en breve para mandar una ambulancia a la zona.")

        elif detected_class == "despedidas":
            res = get_response(ints)
            print(res)
            break

        else:
            res = get_response(ints)
            print(res)


if __name__ == "__main__":
    main()
