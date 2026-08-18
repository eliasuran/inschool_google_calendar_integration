import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.app import App

class GoogleCalendar():
    def __init__(self, app: "App"):
        self.app = app
        self.scopes = ["https://www.googleapis.com/auth/calendar.readonly"]


    def auth(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("google_oauth_client_credentials.json", self.scopes)
                creds = flow.run_local_server(port=0)
            with open("google_oauth_token.json", "w") as token:
                token.write(creds.to_json())

    def create_event(self):
        pass
