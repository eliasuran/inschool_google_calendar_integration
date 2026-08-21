from lib.classes.credentials import Credentials
from lib.classes.fetcher import Fetcher
from lib.classes.google_calendar import GoogleCalendar
from lib.classes.scraper import Scraper


class App():
    def __init__(self):
        self.school_id = "hersleb-vgs"
        self.username: str = "NOT_SET"
        self.password: str = "NOT_SET"
        self.auth_jwt: str | None = "NOT_SET"
        self.scraper = Scraper(self)
        self.credentials = Credentials(self)
        self.google_calendar = GoogleCalendar(self)
        self.fetcher = Fetcher(self)


    def run(self):
        try:
            print("Logger inn..")
            self.auth_jwt = self.scraper.check_and_get_token_from_cache()
            if self.auth_jwt is None:
                self.username, self.password = self.credentials.get_credentials()
                self.auth_jwt = self.scraper.get_auth_jwt_cookie_str()
            self.google_calendar.init()
            print("Henter timeplan fra Visma InSchool..")
            timeplan, start_date, end_date = self.fetcher.get_timeplan_next_x_weeks(4)
            self.google_calendar.create_timeplan_events(timeplan, start_date, end_date)
        except Exception as e:
            raise e
