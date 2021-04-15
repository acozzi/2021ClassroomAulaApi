from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json


SCOPES = ['https://www.googleapis.com/auth/classroom.rosters','https://www.googleapis.com/auth/classroom.profile.emails','https://www.googleapis.com/auth/classroom.profile.photos']

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
    stream2021 = open('updateClassroom.json', 'r', encoding='utf8')
    update2021 = json.load(stream2021)
    stream2021.close()
 
    for aula in update2021:
        id = aula['id']
        aula.pop('id', None)
        course = service.courses().patch(id=id,updateMask='name,section',body=aula).execute()
        print('Course %s updated.' % course.get('name'))
    """
# courses.students.create
    invitacion = {
        "courseId": '279121551912',
        "userId": 'jperez@colegioaula21.edu.ar',
        "role": 'STUDENT'
    }
    
    student = service.invitations().create(body=invitacion).execute()
        
   
"""
    estudiante = {
        'userId': 'test@colegioaula21.edu.ar'
    }
    student = service.courses().students().create(
        courseId='279121551912',
        enrollmentCode='ohhqq3k',
        body=estudiante).execute()
"""
if __name__ == '__main__':
    main()