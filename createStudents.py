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
    
    stream2021 = open('cursoId.json', 'r', encoding='utf8')
    lista2021 = json.load(stream2021)
    stream2021.close()

    grupos2021 = open('grupos.json', 'r', encoding='utf8')
    grupos = json.load(grupos2021)
    grupos2021.close()

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

    #lista2021 json con las aulas
    #grupos json que asocia grupo con user

    for aula in lista2021:
        course = service.courses().get(id=aula['id']).execute()
        enrollment_code = course['enrollmentCode']
        for user in grupos:
            if aula['curso'] == user['Aula']:                
                student = {
                    'userId': user['usuario']
                }
                try:
                    print('Aula>', aula['id'])
                    print('Usuarios', student)
                    student = service.courses().students().create(
                    courseId=aula['id'],
                    enrollmentCode=enrollment_code,
                    body=student).execute()
                    print('''User {%s} was enrolled as a student in
                    the course with ID "{%s}"'''
                    % (student.get('profile').get('name').get('fullName'),
                    aula['id']))
                except:
                    print('You are already a member of this course.')
                   
                   

       
    

     
if __name__ == '__main__':
    main()