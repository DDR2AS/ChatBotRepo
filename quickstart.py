from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

##SETUP OAUTH 2.0 SETUP
#We have to specify some scopes https://developers.google.com/calendar/api/guides/auth
scopes = ['https://www.googleapis.com/auth/calendar.events']

#Then we have to create a flow
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",scopes=scopes)
flow.run_console()