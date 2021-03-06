from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def connect_to_drive(CLIENT_CREDENTIALS, SCOPES):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('data/token.json'):
        creds = Credentials.from_authorized_user_file('data/token.json', SCOPES)
    # If there are no (valid) credentials available, 
    # let the user log in using the brower
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_CREDENTIALS, SCOPES)
            # set the port below to be the same as you redirect uri in gc console
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('data/token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('drive', 'v3', credentials=creds)
        print("drive service created successfully!")
        return service
    except Exception as error:
        print(f'An error occurred: {error}')
        return None


