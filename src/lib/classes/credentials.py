import getpass
import os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.app import App

class Credentials():
    def __init__(self, app: "App"):
        self.app = app

    def get_credentials(self) -> tuple[str, str]:
        if os.getenv("FEIDE_USERNAME") and os.getenv("FEIDE_PASSWORD"):
            username = str(os.getenv("FEIDE_USERNAME"))
            password = str(os.getenv("FEIDE_PASSWORD"))
        else:
            username = input("Brukernavn: ")
            password = getpass.getpass("Passord: ")
        return username, password
