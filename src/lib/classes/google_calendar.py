import datetime
from zoneinfo import ZoneInfo
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


    def _build_event(self, title, location, teacher, date, start_time, end_time):
        date = datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
        return {
            "summary": title,
            "location": location,
            "description": f"{title}.{f' Lærer: {teacher}. ' if teacher is not None else ' '}I rom {location} kl {start_time}.",
            "start": {
                "dateTime": f"{date}T{start_time}:00",
                "timeZone": "Europe/Oslo"
            },
            "end": {
                "dateTime": f"{date}T{end_time}:00",
                "timeZone": "Europe/Oslo"
            },
            "attendees": [],
            "reminders": {
                "useDefault": True,
            }
        }


    def _create_events(self, timeplan_items):
        if self.service is None:
            raise Exception(self.service)
        events = []
        for item in timeplan_items:
            title = item["subject"]
            if title is None:
                title = item.get("label")

            room = item["mainRoom"]
            if room is None and len(item["locations"]) > 0:
                room = item["locations"][0]

            event = self._build_event(
                title,
                room,
                item["teacherName"],
                item["date"],
                item["startTime"],
                item["endTime"],
            )

            events.append(event)

        for i in range(0, len(events), 1000):
            batch = self.service.new_batch_http_request()
            for event in events[i:i + 1000]:
                batch.add(
                    self.service.events().insert(
                        calendarId=self.calendar_id,
                        body=event,
                    )
                )
            batch.execute()

        return len(events)


    def _delete_events(self, start_date, end_date):
        tz = ZoneInfo("Europe/Oslo")
        if self.service is None:
            raise Exception(self.service)
        start_date = start_date - datetime.timedelta(days=start_date.weekday())
        end_date = end_date + datetime.timedelta(days=7 - end_date.weekday())

        time_min = datetime.datetime.combine(
            start_date,
            datetime.time.min,
            tzinfo=tz,
        ).isoformat()
        time_max = datetime.datetime.combine(
            end_date,
            datetime.time.min,
            tzinfo=tz,
        ).isoformat()

        event_ids = []
        page_token = None

        while True:
            response = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                pageToken=page_token,
            ).execute()

            event_ids.extend(
                event["id"]
                for event in response.get("items", [])
            )

            page_token = response.get("nextPageToken")

            if not page_token:
                break

        for i in range(0, len(event_ids), 1000):
            batch = self.service.new_batch_http_request()

            for event_id in event_ids[i:i + 1000]:
                batch.add(
                    self.service.events().delete(
                        calendarId=self.calendar_id,
                        eventId=event_id,
                    )
                )

            batch.execute()

        return len(event_ids)


    def create_timeplan_events(self, timeplan_items, start_date, end_date):
        print("Sletter gamle timer..")
        self._delete_events(start_date, end_date)
        print("Legger til nye timer..")
        self._create_events(timeplan_items)
