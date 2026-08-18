import datetime
import json
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.app import App

class GoogleCalendar():
    def __init__(self, app: "App"):
        self.app = app
        self.token_path = "google_oauth_token.json"
        self.credentials_path = "google_oauth_client_credentials.json"
        self.scopes = ["https://www.googleapis.com/auth/calendar.app.created"]
        self.creds = None
        self.service = None
        self.none_service_exception_message = "No service, auth failed.."
        self.config_path = "config.json"
        self.calendar_id = None

    def init(self):
        if self.creds is None:
            self._auth()
        self.service = build("calendar", "v3", credentials=self.creds)
        self._setup_and_read_config()


    def _setup_and_read_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as file:
                data = json.loads(file.read())
                self.calendar_id = data["calendar_id"]
        else:
            self.calendar_id = self._create_calendar()
            with open(self.config_path, "w") as file:
                json.dump({"calendar_id": self.calendar_id}, file)

    def _auth(self):
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.scopes)
                self.creds = flow.run_local_server(port=0)
            with open(self.token_path, "w") as token:
                token.write(self.creds.to_json())


    def _create_calendar(self):
        if self.service is None:
            raise Exception(self.none_service_exception_message)
        created_calendar = self.service.calendars().insert(body={
            "summary": "Timeplan",
            "description": "Kalender for timeplan"
        }).execute()
        calendar_id = created_calendar["id"]
        return calendar_id

    def _create_event(self):
        if self.service is None:
            raise Exception(self.service)
        event = {
          'summary': 'Google I/O 2015',
          'location': '800 Howard St., San Francisco, CA 94103',
          'description': 'A chance to hear more about Google\'s developer products.',
          'start': {
            'dateTime': '2015-05-28T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
          },
          'end': {
            'dateTime': '2015-05-28T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
          },
          'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
          ],
          'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
          ],
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 10},
            ],
          },
        }

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print("event created:",event.get("htmlLink"))
