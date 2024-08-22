import json
import requests
import time
import random
from tqdm import tqdm
from colorama import Fore, Style, init
from TapMonster import TapMonster

# Inicializar Colorama
init(autoreset=True)

def read_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

def get_wait_time(min_wait, max_wait):
    return random.uniform(min_wait, max_wait)

def print_with_color(message, color):
    print(f"{color}{message}{Style.RESET_ALL}")

def perform_actions(api, buy_until_no_more):
    while True:
        print_with_color("Recuperando datos del usuario...", Fore.YELLOW)
        user_data = api.get_user_data()
        
        # Obtener el número de taps restantes
        taps_remaining = user_data.get('me', {}).get('energy', {}).get('amount', 0)
        print_with_color(f"Taps restantes: {taps_remaining}", Fore.GREEN)

        # Ejecutar taps hasta que queden menos de 100
        while taps_remaining >= 100:
            taps_to_use = random.randint(1, 100)
            time_now = int(time.time() * 1000)  # Tiempo en milisegundos
            current_energy = user_data.get('me', {}).get('energy', {}).get('amount', 0)
            
            print_with_color(f"Ejecutando {taps_to_use} taps...", Fore.CYAN)
            api.tap(taps_to_use, time_now, current_energy)
            user_data = api.get_user_data()
            taps_remaining = user_data.get('me', {}).get('energy', {}).get('amount', 0)

        # Mejorar el elemento más rentable
        while True:
            upgrade_options = user_data.get('me', {}).get('upgrades', [])
            
            if not upgrade_options:
                print_with_color("No hay mejoras disponibles.", Fore.RED)
                break
            
            # Filtrar upgrades con sufficientFunds = true
            purchasable_upgrades = [u for u in upgrade_options if u['nextLevel']['sufficientFunds']]
            
            if not purchasable_upgrades:
                if buy_until_no_more:
                    print_with_color("No hay mejoras disponibles para comprar. Esperando antes de continuar...", Fore.YELLOW)
                    break
                else:
                    print_with_color("No se pueden comprar mejoras con los fondos actuales. Esperando antes de continuar...", Fore.YELLOW)
                    time.sleep(get_wait_time(config['min_wait_time'], config['max_wait_time']))
                    continue
            
            # Elegir la mejora más rentable entre las que se pueden comprar
            best_upgrade = max(purchasable_upgrades, key=lambda x: x['nextLevel']['earnPerHour'] / x['nextLevel']['price'])
            print_with_color(f"Comprando mejora: {best_upgrade['name']}", Fore.GREEN)
            
            if best_upgrade['nextLevel']['price'] > 0:
                response = api.upgrade_element(best_upgrade['slug'])
                print_with_color(f"Respuesta de la compra: {response}", Fore.MAGENTA)
            else:
                print_with_color("No hay fondos suficientes para comprar la mejora más rentable.", Fore.RED)
                break

        # Esperar un tiempo aleatorio antes de la próxima iteración
        config = read_config('config.json')
        wait_time = get_wait_time(config['min_wait_time'], config['max_wait_time'])
        print_with_color(f"Esperando {wait_time:.2f} segundos antes de la próxima iteración...", Fore.YELLOW)
        time.sleep(wait_time)

if __name__ == "__main__":
    config = read_config('config.json')
    api = TapMonster(config['bearer_token'])
    buy_until_no_more = config.get('buy_until_no_more', True)  # Valor predeterminado True si no se especifica
    perform_actions(api, buy_until_no_more)
