import requests
import time
import random
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

class Kuroro:
    def __init__(self, bearer_token):
        self.base_url = "https://ranch-api.kuroro.com/api/Upgrades"
        self.headers = {
            "accept": "application/json",
            "accept-language": "es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "authorization": f"Bearer {bearer_token}",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }

    def fetch_purchasable_upgrades(self):
        url = f"{self.base_url}/GetPurchasableUpgrades"
        response = requests.get(url, headers=self.headers, allow_redirects=True)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def fetch_coins(self):
        url = "https://ranch-api.kuroro.com/api/Game/UpdateCoinsSnapshot"
        response = requests.post(url, headers=self.headers, allow_redirects=True)
        
        if response.status_code == 200:
            data = response.json()
            return data['value']
        else:
            response.raise_for_status()

    def find_most_profitable_upgrade(self, upgrades):
        purchasable_upgrades = [u for u in upgrades if u.get('canBePurchased')]

        if not purchasable_upgrades:
            raise ValueError("No purchasable upgrades found.")

        most_profitable = min(
            purchasable_upgrades,
            key=lambda u: u['cost'] / u['earnIncrement']
        )
        
        return most_profitable

    def buy_upgrade(self, upgrade_id):
        url = f"{self.base_url}/BuyUpgrade"
        payload = {
            "upgradeId": upgrade_id
        }
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def execute(self):
        while True:
            try:
                # Fetch upgrades and coins
                upgrades = self.fetch_purchasable_upgrades()
                coins = self.fetch_coins()

                # Find the most profitable upgrade
                most_profitable = self.find_most_profitable_upgrade(upgrades)
                
                # Check if you have enough coins
                if most_profitable['cost'] > coins:
                    print(Fore.RED + "Not enough coins to purchase the most profitable upgrade.")
                    return

                print(Fore.GREEN + "Most profitable upgrade:")
                print(Fore.GREEN + str(most_profitable))

                # Perform the purchase of the most profitable upgrade
                result = self.buy_upgrade(most_profitable['upgradeId'])
                print(Fore.GREEN + "Purchase result:")
                print(Fore.GREEN + str(result))
                
            except ValueError as e:
                print(Fore.RED + str(e))
                return
            except requests.RequestException as e:
                print(Fore.RED + f"An error occurred: {e}")
                return
            # Wait between 600 and 800 seconds
            wait_time = random.randint(10, 20)
            print(Fore.YELLOW + f"Waiting for {wait_time} seconds...")
            time.sleep(wait_time)
