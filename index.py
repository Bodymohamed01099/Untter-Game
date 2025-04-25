import json
import os
import random
import shutil
from datetime import datetime
from colorama import init, Fore, Back, Style
from Functions.DataManagement import load_data, load_stores, save_data, file_management_menu
from Functions.Game.GameFunctions import show_inventory, buy_from_store, sell_item, atm_menu
from Functions.Game.ATMFunctions import get_details, deposit_balance, withdraw_balance
from Functions.Game.GameFlow import new_game, continue_game, game_loop
from Functions.CoreFunctions import print_header, print_section, print_error

init(autoreset=True)

def ensure_directories():
    for directory in ['./Database', './Database/Players', './Database/Stores']:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print_info(f"Created directory: {directory}")

def print_header():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("  _____ _             _   _       _   _             ")
    print(" |_   _| |__   ___   | | | |_ __ | |_| |_ ___ _ __  ")
    print("   | | | '_ \\ / _ \\  | | | | '_ \\| __| __/ _ \\ '__| ")
    print("   | | | | | |  __/  | |_| | | | | |_| ||  __/ |    ")
    print("   |_| |_| |_|\\___|   \\___/|_| |_|\\__|\\__\\___|_|    ")
    print(f"{Style.RESET_ALL}")

def print_divider():
    print(f"{Fore.YELLOW}{'=' * 50}{Style.RESET_ALL}")

def print_section(title):
    print(f"\n{Fore.GREEN}{Style.BRIGHT}=== {title} ==={Style.RESET_ALL}")

def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")

def main():
    print_header()
    data = load_data()
    
    while True:
        print_section("Main Menu")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} New Game")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Continue Game")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} File Management")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Exit")
        choice = input(f"Select option: {Fore.YELLOW}")
        print(Style.RESET_ALL, end="")
        
        if choice == '1':
            player = new_game(data)
            if player:
                game_loop(player, data)
        elif choice == '2':
            player = continue_game(data)
            if player:
                game_loop(player, data)
        elif choice == '3':
            file_management_menu(data)
        elif choice == '4':
            return
        else:
            print_error("Invalid choice!")

if __name__ == "__main__":
    main()