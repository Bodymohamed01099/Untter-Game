from colorama import Fore, Style
from Functions.DataManagement import save_data, file_management_menu
from Functions.Game.GameFunctions import (
    create_new_player, show_inventory, buy_from_store, 
    sell_item, atm_menu, store_management_menu, check_customer_visit
)
from Functions.CoreFunctions import print_section, print_error, print_success

def new_game(data):
    print_section("New Game")
    
    while True:
        player = create_new_player()
        
        # Check if nickname already exists
        if any(p['nickname'] == player['nickname'] for p in data['players']):
            print_error("Nickname already exists! Please choose a different one.")
            continue
        
        data['players'].append(player)
        save_data(data)
        print_success("New player created successfully!")
        return player

def continue_game(data):
    nickname = input(f"Enter your nickname: {Fore.YELLOW}")
    print(Style.RESET_ALL, end="")
    for player in data['players']:
        if player['nickname'] == nickname:
            return player
    print_error("Player not found!")
    return None

def game_loop(player, data):
    while True:
        print_section("Game Menu")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Inventory")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Buy from Store")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Sell Items")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} ATM")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Store Management")
        print(f"{Fore.CYAN}6.{Style.RESET_ALL} File Management")
        print(f"{Fore.CYAN}7.{Style.RESET_ALL} Save & Exit")
        choice = input(f"Select option: {Fore.YELLOW}")
        print(Style.RESET_ALL, end="")
        
        if choice == '1':
            show_inventory(player)
        elif choice == '2':
            buy_from_store(player)
        elif choice == '3':
            sell_item(player)
        elif choice == '4':
            atm_menu(player)
        elif choice == '5':
            store_management_menu(player)
        elif choice == '6':
            file_management_menu(data, player)
        elif choice == '7':
            for idx, p in enumerate(data['players']):
                if p['nickname'] == player['nickname']:
                    data['players'][idx] = player.copy()
                    save_data(data)
                    print_success("Game saved successfully!")
                    return
            print_error("Error: Player not found in data!")
        else:
            print_error("Invalid choice!")
            
        # Check for customer visits after each action
        check_customer_visit(player) 