from lib.classes.credentials import Credentials
from lib.classes.scraper import Scraper


class App():
    def __init__(self):
        self.school_id = "hersleb-vgs"
        self.username = None
        self.password = None
        self.scraper = Scraper(self)
        self.credentials = Credentials(self)


    def run(self):
        print("run")
        try:
            self.username, self.password = self.credentials.get_credentials()
            self.scraper.get_auth_jwt_cookie_str()
        except Exception as e:
            raise e
