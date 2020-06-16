from __future__ import print_function
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import pickle
import json
import os.path 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

app = Flask(__name__)
CORS(app)

@app.route('/event', methods=["GET", "POST"])
def main(): 

    creds = None
    content = json.loads(request.data)
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

#     service = build('calendar', 'v3', credentials=creds)
#     event={'summary':content['summary'],
#     'location':content['location'],
#     'start':{
#         'dateTime': content['stime'],
#         'timeZone': 'Asia/Kolkata',
#     },
#       'end': {
#           'dateTime': content['etime'],
#           'timeZone': 'Asia/Kolkata',
#   },
#     'attendees': [
#     {'email': content['firstemail']},
#     {'email': content['secondemail']},
#     {'email': content['thirdemail']}
#   ],}
#     event = service.events().insert(calendarId='primary', body=event).execute()
#     print ('Event created: %s' % (event.get('htmlLink')))



    return 'a string'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)