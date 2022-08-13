import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

##SETUP OAUTH 2.0 SETUP
#We have to specify some scopes https://developers.google.com/calendar/api/guides/auth
scopes = ['https://www.googleapis.com/auth/calendar']

#Then we have to create a flow
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",scopes=scopes)
credentials = flow.run_console()

#Then we have to create credential
pickle.dump(credentials,open("token.pkl","wb")) #write binary stream
credentials = pickle.load(open("token.pkl", "rb")) #read
print(credentials)

service = build("calendar","v3",credentials=credentials)

result = service.calendarList().list().execute()


print(result['items'][2])
#Imprimimos todas las keys del diccionario de resultados
print(result['items'][2].keys())

#for i in range(0,len(result['items'])):
#    print(result['items'][i])

#Obtener eventos del calendario
calendar_id = result['items'][2]['id']
print(calendar_id)
result = service.events().list(calendarId=calendar_id,timeZone = "America/Bogota").execute()
print('\n')
print(result)


#Creación de evento
from datetime import datetime, timedelta
start_time = datetime(2022, 8, 12, 19, 30, 0)
end_time = start_time + timedelta(hours=2)

print(f'Start time {start_time}')
print(f'time delta = {timedelta(hours=4)}\n End time  = {end_time}')

#Body of the event
def CreateBodyEvent(summary,location,description,startTime,endTime,TimeZone):
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

timezone = "America/Bogota"

#Usando nuestra función
event = CreateBodyEvent('Cita con caardiologo','Hosp. Almenara','Consulta general',start_time,end_time,timezone)
service.events().insert(calendarId=calendar_id, body=event).execute()