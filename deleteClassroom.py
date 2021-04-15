from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

SCOPES = ['https://www.googleapis.com/auth/classroom.courses']

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    
    #stream2021 = open('updateClassroom.json', 'r', encoding='utf8')
    #update2021 = json.load(stream2021)
    #stream2021.close()
    deletes = [
        {'id': '279105186572'},
        {'id': '279123852394'},
        {'id': '279123459656'}
    ]
    ### Falta la precondicion de archivar el curso
    for aula in deletes:
        print(aula)
        course = service.courses().delete(id=aula).execute()
        print('Course %s updated.' % course.get('name'))



if __name__ == '__main__':
    main()