import requests
import json

class TapMonster:
    def __init__(self, bearer_token):
        self.headers = {
            'accept-language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'authorization': f'Bearer {bearer_token}',
            'content-type': 'application/json',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site'
        }

    def get_user_data(self):
        url = "https://api.tapmonsters.wombat.app/me"
        response = requests.post(url, headers=self.headers)
        return response.json()

    def upgrade_element(self, slug):
        url = "https://api.tapmonsters.wombat.app/upgrades"
        payload = json.dumps({"slug": slug})
        response = requests.post(url, headers=self.headers, data=payload)
        return response.json()

    def tap(self, taps, time, current_energy):
        url = "https://api.tapmonsters.wombat.app/batch-tap"
        payload = json.dumps({
            "taps": taps,
            "time": time,
            "currentEnergy": current_energy
        })
        response = requests.post(url, headers=self.headers, data=payload)
        return response.json()
    
    def login_streak(self):
        url = "https://api.tapmonsters.wombat.app/login-streak"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def login_streak_collect(self, number):
        url = "https://api.tapmonsters.wombat.app/login-streak"
        payload = json.dumps({
            "number": number
        })
        response = requests.post(url, headers=self.headers, data=payload)
        return response.json()

