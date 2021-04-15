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

    
    stream2020 = open('aulas2020.json', 'r', encoding='utf8')
    aulas2020 = json.load(stream2020)
    stream2020.close()
    for ids in aulas2020:
        try:
            course = service.courses().get(id=ids['id']).execute()
            course['courseState'] = 'ARCHIVED'
            course = service.courses().update(id=ids['id'], body=course).execute()
        except:
            print('Error con el curso ', ids)
        #
        #if ids['courseState'] == 'ARCHIVED':
        #course = service.courses().update(id=ids['id'], body=course).execute()
        #print('Course %s updated.' % course.get('name'))
        #print(ids['name'],' ',ids['courseState'])




    """
    # load an object into the course variable
    course = service.courses().get(id='142251492980').execute()
    # modify the buffer
    course['courseState'] = 'ACTIVE'
    # update the buffen inside the server
    course = service.courses().update(id=142251492980, body=course).execute()
    print('Course %s updated.' % course.get('name'))
    """

if __name__ == '__main__':
    main()