from __future__ import print_function
import datetime
from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r'/*': {'origins': '*'}})
@app.route('/event', methods=["GET", "POST"])
def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    content = json.loads(request.data)
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
            creds = flow.run_local_server(port=80)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    if(service):

            event = {
            'summary': content['summary'],
            'location': content['location'],
            'start': {
                'dateTime': content['stime']+":00",
                'timeZone': 'Asia/Kolkata',
                },
            'end': {
                'dateTime': content['etime'] + ":00",
                'timeZone': 'Asia/Kolkata',
                },
            'attendees': [
                {'email':content['firstemail']},
                {'email': content['secondemail']},
                {'email': content['thirdemail']}
                  ]
        }
            event = service.events().insert(calendarId='primary', body=event).execute()
            print ('Event created: %s' % (event.get('htmlLink')))
            return ("Event created")


    else:
        return("Event not created pls try after some time")




if __name__ == '__main__':
    app.run(threaded=True, debug=True)