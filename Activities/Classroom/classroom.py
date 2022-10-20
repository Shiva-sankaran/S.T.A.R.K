from __future__ import print_function
import pickle
import os.path
import json as simplejson
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors
import datetime,time


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/classroom.rosters','https://www.googleapis.com/auth/classroom.courses','https://www.googleapis.com/auth/classroom.coursework.me']
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

def intialize_api():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('classroom', 'v1', credentials=creds)


def create_aliases():
    if os.path.exists('config.pickle'):
        os.remove("config.pickle")
    courses_data = {}
    service = intialize_api()
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])
    if not courses:
           print('No courses found.')
    else:
        for course in courses:
            alias = input("custom name for {} :".format(course['name']))
            if alias != 'NA':
                courses_data[alias] = course['id']
    print(courses_data)
    with open('config.pickle', 'wb') as f:
         pickle.dump(courses_data, f)

def check_for_assignments():
    flag = 0
    service = intialize_api()
    with open('config.pickle', 'rb') as f:
        data = pickle.load(f)
    for alias_name,Id in data.items():
        results = service.courses().courseWork().list(courseId = Id).execute()
        assignments = results.get('courseWork',[])
        for assignment in assignments:
            if assignment['workType'] == 'ASSIGNMENT' and 'dueDate' in assignment.keys() and 'dueTime' in assignment.keys():
                due = tuple(assignment['dueDate'].values()) + tuple(assignment['dueTime'].values())
                due_date = datetime.datetime(*due)
                if due_date >= datetime.datetime.now():
                    flag =1 
                    try:
                        print("assignment in {}:{} on {}".format(alias_name,assignment['title'],utc_to_local(due_date)))
                    except:
                        print("ERROR!")
    if flag == 0:
        print("No assignments due soon")

