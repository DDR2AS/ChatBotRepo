import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import datefinder
from datetime import datetime, timedelta
def setupGoogleCalendar():

    #SETUP OAUTH 2.0 SETUP
    #We have to specify some scopes https://developers.google.com/calendar/api/guides/auth
    scopes = ['https://www.googleapis.com/auth/calendar']

    #Then we have to create a flow
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",scopes=scopes)
    credentials = flow.run_console()

    #Then we have to create credential
    pickle.dump(credentials,open("token.pkl","wb")) #write binary stream
    credentials = pickle.load(open("token.pkl", "rb")) #read
    print(credentials)
    service = build("calendar", "v3", credentials=credentials)
    return service

#Creación del evento
def CreateEvent(id,service,strDateAppointment,summary, description = None,duration = 0.5, location = 'America/Bogota'):

    #En la descripción va el hospital donde es la cita, el nombre del paciente.
    matches = list(datefinder.find_dates(strDateAppointment))
    if len(matches):
        #Intervalo de tiempo de duración de 30 minutos para cada cita
        delta = timedelta(hours=duration)
        #La fecha encontrada no debe ser nulo
        HoraInicio = matches[0]
        HoraFin = HoraInicio + delta

        #Creamos el cuerpo
        event = CreateBodyEvent(summary,description,location,HoraInicio,HoraFin,location)
        #Se añade al calendar el evento
        service.events().insert(calendarId=id, body=event).execute()
        return event



#Body of the event
def CreateBodyEvent(summary,description,location,startTime,endTime,TimeZone):
    eventBody = {
      'summary': summary,
      'location': location,
      'description': description,
      'start': {
        'dateTime': startTime.strftime("%Y-%m-%dT%H:%M:%S"),
        'timeZone': TimeZone,
      },
      'end': {
        'dateTime': endTime.strftime("%Y-%m-%dT%H:%M:%S"),
        'timeZone': TimeZone,
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }
    return eventBody

import requests
import json
def VerificarIdentidad(dni):
    url = "https://www.softwarelion.xyz/api/reniec/reniec-dni"
    _json = { "dni": dni }
    token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNzE3LCJjb3JyZW8iOiJkaWVnby5hdmlsYTEyMzk0QGdtYWlsLmNvbSIsImlhdCI6MTY2MDQwMDYxNX0.lRhe0yQd2LdxUlKA_o4FNVj3TCTnnNvpLClCVEzgZLw"
    _headers = {'Content-Type' : 'application/json' ,'Authorization': token}
    response  = requests.post(url,data=json.dumps(_json), headers= _headers)

    #Convertimos a json para poder acceder a ellos
    return response
    print(response.content)
    print(dataJson.keys)

def consultNameOwner(dni):
    response = VerificarIdentidad(dni)
    dataJson = response.json()
    if dataJson['success']:
        strName = dataJson['result']['nombres'] + " " + dataJson['result']['paterno'] + " " + dataJson['result']['materno']
        result = {'success': True, 'Names': strName}
        return result
    else:
        result = {'success': False, 'Names': ''}
        return
'''
#Imprimimos todas las keys del diccionario de resultados
print(result['items'][2].keys())

#for i in range(0,len(result['items'])):
#    print(result['items'][i])

#Obtener eventos del calendario
calendar_id = result['items'][2]['id']
print(calendar_id)
result = service.events().list(calendarId=calendar_id,timeZone = "America/Bogota").execute()
print(result)

#Creación de evento
from datetime import datetime, timedelta
start_time = datetime(2022, 8, 12, 19, 30, 0)
end_time = start_time + timedelta(hours=2)

print(f'Start time {start_time}')
print(f'time delta = {timedelta(hours=4)}\n End time  = {end_time}')



timezone = "America/Bogota"

#Usando nuestra función
event = CreateBodyEvent('Cita con caardiologo','Hosp. Almenara','Consulta general',start_time,end_time,timezone)


'''
