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

for i in range(0,len(result['items'])):
    print(result['items'][i]['summary'])

