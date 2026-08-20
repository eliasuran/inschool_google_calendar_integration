import requests
import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.app import App

class Fetcher():
    def __init__(self, app: "App"):
        self.app = app
        self.school_id = app.school_id
        self.numba = 10355483 #ingen anelse hva dette tallet betyr. bruker ID? kan dette hentes et sted, og vil det endre seg? forskjellig per bruker?
        self.url = f"https://{self.school_id}.inschool.visma.no/control/timetablev2/learner/{self.numba}/fetch/ALL/0/current?extra-info=true&types=LESSON,EVENT,ACTIVITY,SUBSTITUTION"

    
    def _call_visma_api(self, url):
        headers = {
            "Content-Type":"application/json",
            "Authorization": f"Bearer {self.app.auth_jwt}"
        }
        res = requests.get(url,headers=headers)
        print(res.text)
        return res.json()


    def _get_timeplan(self, for_week_date):
        data = self._call_visma_api(self.url+f"&forWeek={for_week_date}")
        return data.get("timetableItems",[])


    def get_timeplan_next_4_weeks(self):
        timeplan_items = []
        now = datetime.datetime.now()
        for i in range(4):
            for_week_date = (now + datetime.timedelta(days=7*i)).strftime("%d/%m/%Y")
            items = self._get_timeplan(for_week_date)
            timeplan_items.append(items)
        return timeplan_items
