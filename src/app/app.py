from lib.classes.credentials import Credentials
from lib.classes.scraper import Scraper


class App():
    def __init__(self):
        self.school_id = "hersleb-vgs"
        self.username: str = "NOT_SET"
        self.password: str = "NOT_SET"
        self.auth_jwt: str | None = "NOT_SET"
        self.scraper = Scraper(self)
        self.credentials = Credentials(self)


    def run(self):
        try:
            self.auth_jwt = self.scraper.check_and_get_token_from_cache()
            if self.auth_jwt is None:
                self.username, self.password = self.credentials.get_credentials()
                self.auth_jwt = self.scraper.get_auth_jwt_cookie_str()
            print("auth jwt:",self.auth_jwt)
        except Exception as e:
            raise e
