from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

SCOPES = ['https://www.googleapis.com/auth/classroom.topics']

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

    """
    stream2021 = open('listaClassrooms.json', 'r', encoding='utf8')
    lista2021 = json.load(stream2021)
    stream2021.close()
    """

    topics = [
        {"name": '1° Bimestre'},
        {"name": '2° Bimestre'},
        {"name": '3° Bimestre'},
        {"name": '4° Bimestre'},
        {"name": 'Insumos'}
        ]
    
    
    for aula in lista2021:
        response = service.courses().topics().create(
            courseId=aula,
            body=topics[4]).execute()
        
if __name__ == '__main__':
    main()
