from playwright.sync_api import sync_playwright
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.app import App

class Scraper():
    def __init__(self, app: "App"):
        self.app = app
        self.school_id = app.school_id
        self.url = f"https://{self.school_id}.inschool.visma.no/#/app/dashboard"

    def get_auth_jwt_cookie_str(self):
        print("USERNAME:",self.app.username)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.url)
            cookies = context.cookies()
            print(cookies)
            browser.close()
