from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from googleapiclient.errors import HttpError

SCOPES = [
'https://www.googleapis.com/auth/classroom.rosters',
'https://www.googleapis.com/auth/classroom.profile.emails',
'https://www.googleapis.com/auth/classroom.courses',
'https://www.googleapis.com/auth/classroom.profile.photos']

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
                'cred.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    
    stream2021 = open('teacher.json', 'r', encoding='utf8')
    lista2021 = json.load(stream2021)
    stream2021.close()
    
    

    for aula in lista2021:
    
        teacher = {'userId': aula['teacher']}
        try:
            teachers = service.courses().teachers()
            teacher = teachers.create(courseId=aula['id'],
                              body=teacher).execute()
            print('User %s was added as a teacher to the course with ID %s'
             % (teacher.get('profile').get('name').get('fullName'),
             lista2021['id']))
        except:
            print('User is already a member of this course.')
    


            
     
if __name__ == '__main__':
    main()