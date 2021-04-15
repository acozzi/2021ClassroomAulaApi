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

    
    stream2021 = open('crear2clasicas.json', 'r', encoding='utf8')
    aulas2021 = json.load(stream2021)
    stream2021.close()
    print(aulas2021[0]['name'])

    for aula in aulas2021:
        course = service.courses().create(body=aula).execute()
        print('Course %s updated.' % course.get('id'))
        aula['id'] = course.get('id')

    outfile = open('outfile2.json', 'w', encoding='utf8')
    outfile.write(json.dumps(aulas2021))
    outfile.close()

    # load an object into the course variable
    """
    test = {
        "name": "prueba12021",
        "section": "tics2021",
        "ownerId": "tics@colegioaula21.edu.ar",
    }
    """ 
    



if __name__ == '__main__':
    main()