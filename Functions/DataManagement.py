import json
import os
import shutil
from datetime import datetime
from colorama import Fore, Style
from Functions.CoreFunctions import print_section, print_success, print_error, print_info

# Constants
GAME_DATA_FILE = './Database/game_data.json'
STORES_FILE = './Database/Stores/stores.json'

def ensure_directories():
    for directory in ['../Database', '../Database/Players', '../Database/Stores']:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"{Fore.BLUE}ℹ Created directory: {directory}{Style.RESET_ALL}")

def load_data():
    ensure_directories()
    if os.path.exists(GAME_DATA_FILE):
        try:
            with open(GAME_DATA_FILE, 'r') as f:
                data = json.load(f)
                if 'players' not in data:
                    data['players'] = []
                if clean_duplicate_players(data):
                    print_info("Cleaned up duplicate players in the database.")
                return data
        except json.JSONDecodeError:
            print(f"{Fore.RED}✗ Error reading game data. Creating new file.{Style.RESET_ALL}")
            return {'players': []}
    return {'players': []}

def load_stores():
    ensure_directories()
    if os.path.exists(STORES_FILE):
        try:
            with open(STORES_FILE, 'r') as f:
                data = json.load(f)
                if 'stores' not in data:
                    data['stores'] = {}
                return data['stores']
        except json.JSONDecodeError:
            print(f"{Fore.RED}✗ Error reading stores data. Creating new file.{Style.RESET_ALL}")
            return {}
    return {}

def save_data(data):
    ensure_directories()
    try:
        with open(GAME_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"{Fore.RED}✗ Error saving game data: {str(e)}{Style.RESET_ALL}")

def list_saved_files():
    print(f"\n{Fore.GREEN}=== Saved Files ==={Style.RESET_ALL}")
    if not os.path.exists('saves'):
        os.makedirs('saves')
        print(f"{Fore.BLUE}ℹ No saved files found!{Style.RESET_ALL}")
        return []
    
    files = [f for f in os.listdir('saves') if f.endswith('.json')]
    if not files:
        print(f"{Fore.BLUE}ℹ No saved files found!{Style.RESET_ALL}")
        return []
    
    for idx, file in enumerate(files, 1):
        file_path = os.path.join('saves', file)
        size = os.path.getsize(file_path)
        modified = datetime.fromtimestamp(os.path.getmtime(file_path))
        print(f"{Fore.CYAN}{idx}. {file} - Size: {size} bytes - Last Modified: {modified}{Style.RESET_ALL}")
    return files

def create_backup():
    if not os.path.exists(GAME_DATA_FILE):
        print(f"{Fore.RED}✗ No game data to backup!{Style.RESET_ALL}")
        return
    
    backup_dir = os.path.join('./Database', 'backups')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'game_backup_{timestamp}.json'
    shutil.copy2(GAME_DATA_FILE, os.path.join(backup_dir, backup_file))
    print(f"{Fore.GREEN}✓ Backup created: {backup_file}{Style.RESET_ALL}")

def delete_save_file(filename):
    file_path = os.path.join('saves', filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{Fore.GREEN}✓ Deleted save file: {filename}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ File not found!{Style.RESET_ALL}")

def export_game_data(player):
    export_dir = os.path.join('./Database', 'exports')
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    export_file = f'export_{player["nickname"]}_{timestamp}.json'
    with open(os.path.join(export_dir, export_file), 'w') as f:
        json.dump(player, f, indent=4)
    print(f"{Fore.GREEN}✓ Game data exported to: {export_file}{Style.RESET_ALL}")

def import_game_data():
    export_dir = os.path.join('./Database', 'exports')
    if not os.path.exists(export_dir):
        print(f"{Fore.RED}✗ No exports directory found!{Style.RESET_ALL}")
        return None
    
    files = [f for f in os.listdir(export_dir) if f.endswith('.json')]
    if not files:
        print(f"{Fore.RED}✗ No export files found!{Style.RESET_ALL}")
        return None
    
    print(f"\n{Fore.GREEN}=== Available Exports ==={Style.RESET_ALL}")
    for idx, file in enumerate(files, 1):
        print(f"{Fore.CYAN}{idx}. {file}{Style.RESET_ALL}")
    
    try:
        choice = int(input(f"Select file to import (0 to cancel): {Fore.YELLOW}"))
        print(Style.RESET_ALL, end="")
        if choice == 0: return None
        selected_file = files[choice-1]
        
        with open(os.path.join(export_dir, selected_file), 'r') as f:
            imported_player = json.load(f)
            
            # Validate the imported player data
            required_fields = ['name', 'type', 'nickname', 'cash', 'visa', 'inventory', 'shops']
            if not all(field in imported_player for field in required_fields):
                print(f"{Fore.RED}✗ Invalid player data format!{Style.RESET_ALL}")
                return None
            
            print_section("Current Player Data")
            print(f"{Fore.CYAN}Name:{Style.RESET_ALL} {imported_player['name']}")
            print(f"{Fore.CYAN}Type:{Style.RESET_ALL} {imported_player['type']}")
            print(f"{Fore.CYAN}Nickname:{Style.RESET_ALL} {imported_player['nickname']}")
            print(f"{Fore.GREEN}Cash:{Style.RESET_ALL} {imported_player['cash']}")
            print(f"{Fore.BLUE}Visa:{Style.RESET_ALL} {imported_player['visa']}")
            
            if input(f"\nEdit player data? (y/n): {Fore.YELLOW}").lower() == 'y':
                print(Style.RESET_ALL, end="")
                imported_player['name'] = input(f"Enter new name [{imported_player['name']}]: {Fore.YELLOW}") or imported_player['name']
                print(Style.RESET_ALL, end="")
                imported_player['type'] = input(f"Enter new type [{imported_player['type']}]: {Fore.YELLOW}") or imported_player['type']
                print(Style.RESET_ALL, end="")
                
                while True:
                    new_nickname = input(f"Enter new nickname [{imported_player['nickname']}]: {Fore.YELLOW}") or imported_player['nickname']
                    print(Style.RESET_ALL, end="")
                    if new_nickname == imported_player['nickname']:
                        break
                    
                    data = load_data()
                    if any(p['nickname'] == new_nickname for p in data['players']):
                        print(f"{Fore.RED}✗ This nickname already exists!{Style.RESET_ALL}")
                        continue
                    imported_player['nickname'] = new_nickname
                    break
                
                try:
                    new_cash = input(f"Enter new cash amount [{imported_player['cash']}]: {Fore.YELLOW}")
                    print(Style.RESET_ALL, end="")
                    if new_cash:
                        imported_player['cash'] = float(new_cash)
                    
                    new_visa = input(f"Enter new visa amount [{imported_player['visa']}]: {Fore.YELLOW}")
                    print(Style.RESET_ALL, end="")
                    if new_visa:
                        imported_player['visa'] = float(new_visa)
                except ValueError:
                    print(f"{Fore.RED}✗ Invalid amount entered!{Style.RESET_ALL}")
                    return None
                
                print_success("Player data updated successfully!")
            
            return imported_player
            
    except (ValueError, IndexError):
        print(f"{Fore.RED}✗ Invalid choice!{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}✗ Error importing file: {str(e)}{Style.RESET_ALL}")
        return None

def file_management_menu(data, player=None):
    while True:
        print(f"\n{Fore.GREEN}=== File Management ==={Style.RESET_ALL}")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} List Saved Files")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Create Backup")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Delete Save File")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Export Game Data")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Import Game Data")
        print(f"{Fore.CYAN}6.{Style.RESET_ALL} Back")
        choice = input(f"Select option: {Fore.YELLOW}")
        print(Style.RESET_ALL, end="")
        
        if choice == '1':
            list_saved_files()
        elif choice == '2':
            create_backup()
        elif choice == '3':
            files = list_saved_files()
            if files:
                try:
                    choice = int(input(f"Select file to delete (0 to cancel): {Fore.YELLOW}"))
                    print(Style.RESET_ALL, end="")
                    if choice == 0: continue
                    delete_save_file(files[choice-1])
                except:
                    print(f"{Fore.RED}✗ Invalid choice!{Style.RESET_ALL}")
        elif choice == '4':
            if player:
                export_game_data(player)
            else:
                print(f"{Fore.RED}✗ No active game to export!{Style.RESET_ALL}")
        elif choice == '5':
            imported_data = import_game_data()
            if imported_data:
                data['players'].append(imported_data)
                save_data(data)
                print(f"{Fore.GREEN}✓ Game data imported successfully!{Style.RESET_ALL}")
        elif choice == '6':
            break
        else:
            print(f"{Fore.RED}✗ Invalid option!{Style.RESET_ALL}")

def clean_duplicate_players(data):
    """Remove duplicate players based on nickname"""
    unique_players = {}
    for player in data['players']:
        nickname = player['nickname']
        if nickname not in unique_players:
            unique_players[nickname] = player
    
    data['players'] = list(unique_players.values())
    save_data(data)
    return len(data['players']) != len(unique_players)