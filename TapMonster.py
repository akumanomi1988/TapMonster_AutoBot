import requests
import json
import time

class TapMonster:
    def __init__(self, query_id):
        self.query_id = query_id
        self.token = None
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'x-tm-api-version': '1.1.0'
        }

    def login(self):
        """Fetches a new token using the query_id."""
        url = "https://api.tapmonsters.wombat.app/login"
        payload = json.dumps({
            "initData": self.query_id  # The full query_id string is used directly here
        })
        response = requests.post(url, headers=self.headers, data=payload)
        
        if response.status_code == 200:
            self.token = response.json().get('token')
            if self.token:
                self.headers['authorization'] = f'Bearer {self.token}'
                print("Login successful, token updated.")
            else:
                raise Exception("Failed to retrieve token from login response.")
        else:
            raise Exception(f"Error during login process: {response.status_code} - {response.text}")

    def request_with_token(self, url, method="POST", data=None):
        """Makes a request using the token. If unauthorized (401), logs in again."""
        if not self.token:
            self.login()  # Fetch token at startup

        response = requests.request(method, url, headers=self.headers, data=data)
        
        # If token expired or is invalid, attempt re-login
        if response.status_code == 401:
            print("Token expired, logging in again...")
            self.login()  # Retry login
            response = requests.request(method, url, headers=self.headers, data=data)
        
        return response.json()

    def get_user_data(self):
        """Calls the API to get user data."""
        url = "https://api.tapmonsters.wombat.app/me"
        return self.request_with_token(url)

    def upgrade_element(self, slug):
        """Calls the API to upgrade an element."""
        url = "https://api.tapmonsters.wombat.app/upgrades"
        payload = json.dumps({"slug": slug})
        return self.request_with_token(url, data=payload)

    def tap(self, taps, time, current_energy):
        """Calls the API to perform taps."""
        url = "https://api.tapmonsters.wombat.app/batch-tap"
        payload = json.dumps({
            "taps": taps,
            "time": time,
            "currentEnergy": current_energy
        })
        return self.request_with_token(url, data=payload)

    def login_streak(self):
        """Calls the API to get login streak information."""
        url = "https://api.tapmonsters.wombat.app/login-streak"
        return self.request_with_token(url, method="GET")

    def login_streak_collect(self, number):
        """Calls the API to collect a login streak reward."""
        url = "https://api.tapmonsters.wombat.app/login-streak"
        payload = json.dumps({"number": number})
        return self.request_with_token(url, data=payload)
    
    def refill_energy(self):
        """Attempt to refill energy."""
        response = requests.post(f"{self.base_url}/energy/refill", headers=self.headers)
        return response.json()