import json
import requests
import time
import random
from colorama import Fore, Style, init
from TapMonster import TapMonster
from kuroro import Kuroro
import math

# Initialize Colorama
init(autoreset=True)

def read_config(config_file):
    """Read configuration from a JSON file."""
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        print_with_color(f"Error reading config file: {e}", Fore.RED)
        raise

def get_wait_time(min_wait, max_wait):
    """Generate a random wait time between min_wait and max_wait."""
    return random.uniform(min_wait, max_wait)

def print_with_color(message, color):
    """Print message with specified color."""
    print(f"{color}{message}{Style.RESET_ALL}")

def get_user_data(api:TapMonster):
    """Retrieve user data from the API."""
    try:
        print_with_color("Retrieving user data...", Fore.YELLOW)
        return api.get_user_data()
    except requests.RequestException as e:
        print_with_color(f"Error retrieving user data: {e}", Fore.RED)
        raise

def execute_taps(api:TapMonster, user_data):
    """Execute taps until fewer than 100 remain."""
    taps_remaining = user_data.get('me', {}).get('energy', {}).get('amount', 0)
    
    while taps_remaining >= 100:
        taps_to_use = random.randint(10, 100)
        print_with_color(f"Executing {taps_to_use} taps...", Fore.CYAN)
        time.sleep(math.floor(taps_to_use / 10))
        time_now = int(time.time() * 1000)  # Time in milliseconds
        current_energy = user_data.get('me', {}).get('energy', {}).get('amount', 0)

        try:
            response = api.tap(taps_to_use, time_now, current_energy)
            user_data = response  # Update user_data with the latest response
        except requests.RequestException as e:
            print_with_color(f"Error executing taps: {e}", Fore.RED)
            continue
        
        taps_remaining = user_data.get('me', {}).get('energy', {}).get('amount', 0)

def purchase_upgrades(api:TapMonster, buy_until_no_more, config):
    """Purchase the most cost-effective upgrades."""
    while True:
        time.sleep(5)
        user_data = get_user_data(api)
        upgrade_options = user_data.get('me', {}).get('upgrades', [])

        if not upgrade_options:
            print_with_color("No upgrades available.", Fore.RED)
            break

        # Filter upgrades with sufficient funds, level > 0, and next level > 0
        purchasable_upgrades = [
            u for u in upgrade_options
            if u['nextLevel']['sufficientFunds']
            and u['level'] > 0
            and u['nextLevel']['price'] > 0
        ]

        if not purchasable_upgrades:
            if buy_until_no_more:
                print_with_color("No upgrades available to buy. Waiting before continuing...", Fore.YELLOW)
                break
            else:
                print_with_color("No affordable upgrades. Waiting before continuing...", Fore.YELLOW)
                break

        # Choose the most cost-effective upgrade among those that can be purchased
        best_upgrade = max(
            purchasable_upgrades,
            key=lambda x: x['nextLevel']['earnPerHour'] / x['nextLevel']['price']
        )
        print_with_color(f"Purchasing upgrade: {best_upgrade['name']} :: {best_upgrade['slug']}", Fore.GREEN)

        try:
            response = api.upgrade_element(best_upgrade['slug'])
            # Only print the response if there is an error
            if 'message' in response and response['message']:
                print_with_color(f"Purchase response: {response}", Fore.RED)
            # Update user_data with the latest response
            user_data = response
        except requests.RequestException as e:
            print_with_color(f"Error purchasing upgrade: {e}", Fore.RED)
            break
        # Continue from the start of the loop
        continue
def collect_daily_streak(api: TapMonster):
    try:
        print_with_color("Getting streak status",color=Fore.YELLOW)
        response = api.login_streak()
        if len(response) > 1:
            collectable_entries = list(filter(lambda entry: entry['state'] == "COLLECTABLE", response['entries']))
            if collectable_entries:
                api.login_streak_collect(collectable_entries[0]['number'])
                print_with_color(f"Collected element: {collectable_entries[0]['number']}",color=Fore.GREEN)
                return
        print_with_color(f"No collectable elements.",color=Fore.YELLOW)
    except requests.RequestException as e:
        print_with_color(f"Error obtain streak status: {e}", Fore.RED)
        


def perform_actions(tapmonster:TapMonster,kuroro:Kuroro, buy_until_no_more, config):
    """Perform the main actions: tapping and upgrading."""
    errCount = 0
    while True:
        try:
            user_data = get_user_data(tapmonster)
            execute_taps(tapmonster, user_data)
            purchase_upgrades(tapmonster, buy_until_no_more, config)
            collect_daily_streak(tapmonster)
            wait_time = get_wait_time(config['min_wait_time'], config['max_wait_time'])
            print_with_color(f"Waiting {wait_time:.2f} seconds before next iteration...", Fore.YELLOW)
            kuroro.execute()
            time.sleep(wait_time)
        except:
            errCount +=1
            if errCount < 5:
                continue

if __name__ == "__main__":
    try:
        config = read_config('config.json')
        tapmonster_api = TapMonster(config['tapmonster_bearer_token'])
        kuroro_api = Kuroro(config['kuroro_bearer_token'])
        buy_until_no_more = config.get('buy_until_no_more', True)  # Default to True if not specified
        perform_actions(tapmonster_api,kuroro_api, buy_until_no_more, config)
    except Exception as e:
        print_with_color(f"An unexpected error occurred: {e}", Fore.RED)
