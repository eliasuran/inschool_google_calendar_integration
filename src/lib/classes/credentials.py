import getpass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.app import App

class Credentials():
    def __init__(self, app: "App"):
        self.app = app

    def get_credentials(self) -> tuple[str, str]:
        username = input("Brukernavn: ")
        password = getpass.getpass("Passord: ")
        return username, password
