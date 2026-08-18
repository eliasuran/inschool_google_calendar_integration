import json
import time
from playwright.sync_api import sync_playwright
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.app import App

class Scraper():
    def __init__(self, app: "App"):
        self.app = app
        self.school_id = app.school_id
        self.url = f"https://{self.school_id}.inschool.visma.no/#/app/dashboard"
        self.token_cache_path = "inschool_tokens_cache.json"
        self.token_expiry_seconds = 3600 * 2

    def get_auth_jwt_cookie_str(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.url)
            page.locator('#onetrust-reject-all-handler').click()
            page.locator('#login-with-feide-button').click()

            page.locator('#username').fill(self.app.username)
            page.locator('#password').fill(self.app.password)

            page.locator('.button-primary').click()
            
            page.get_by_text("Timeplan").wait_for()

            cookies = context.cookies()
            auth_jwt = None
            for cookie in cookies:
                if cookie.get("name") == "Authorization":
                    auth_jwt = cookie.get("value")
            if auth_jwt is None:
                raise Exception("no auth cookie found")
            self._store_token_in_cache(auth_jwt)
            browser.close()
        return auth_jwt


    def check_and_get_token_from_cache(self):
        with open(self.token_cache_path, "r", encoding="utf-8") as file:
            content = file.read()
            if "{" not in content:
                 return None #}
            data = json.loads(content)
            if data.get("expires",0) > time.time():
                return data.get("token")
            return None


    def _store_token_in_cache(self, token):
        data = {
            "token": token,
            "expires": time.time() + self.token_expiry_seconds
        }
        with open(self.token_cache_path, "w") as file:
            json.dump(data, file)
