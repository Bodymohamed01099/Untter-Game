import random
import json
from colorama import Fore, Style
from Functions.DataManagement import load_stores
from Functions.CoreFunctions import print_section, print_success, print_error, print_info, print_warning
from Functions.Game.GameUtils import (
    format_item, calculate_sell_price, validate_amount,
    STARTING_CASH, STARTING_VISA, STREET_SALE_CHANCE
)
from Functions.Game.ATMFunctions import get_details, deposit_balance, withdraw_balance
from datetime import datetime

def load_store_locations():
    try:
        with open('Database/Stores/store_locations.json', 'r') as f:
            return json.load(f)['locations']
    except:
        print_error("Error loading store locations!")
        return []

def show_inventory(player):
    print_section("Inventory")
    if not player['inventory']:
        print_info("Empty")
    else:
        for idx, item in enumerate(player['inventory'], 1):
            print(f"{Fore.CYAN}{idx}. {format_item(item)}{Style.RESET_ALL}")

def buy_from_store(player):
    stores = load_stores()
    if not stores:
        print_error("No stores available!")
        return
    
    print_section("Available Stores")
    for idx, store in enumerate(stores, 1):
        print(f"{Fore.CYAN}{idx}. {store}{Style.RESET_ALL}")
    
    try:
        choice = int(input(f"Select store (0 to cancel): {Fore.YELLOW}"))
        print(Style.RESET_ALL, end="")
        if choice == 0: return
        store_name = list(stores.keys())[choice-1]
        store = stores[store_name]
    except:
        print_error("Invalid choice!")
        return

    print_section(store_name)
    for idx, item in enumerate(store['items'], 1):
        print(f"{Fore.CYAN}{idx}. {format_item(item)} - {item['price']} {store['payment']}{Style.RESET_ALL}")
    
    try:
        item_choice = int(input(f"Select item (0 to cancel): {Fore.YELLOW}"))
        print(Style.RESET_ALL, end="")
        if item_choice == 0: return
        selected = store['items'][item_choice-1]
    except:
        print_error("Invalid choice!")
        return

    if player[store['payment']] < selected['price']:
        print_error("Insufficient funds! Visit ATM?")
        if input(f"Go to ATM? (y/n): {Fore.YELLOW}").lower() == 'y':
            print(Style.RESET_ALL, end="")
            atm_menu(player)
        return
    
    player[store['payment']] -= selected['price']
    player['inventory'].append({
        'name': selected['name'],
        'value': selected['price']//2,
        'type': selected['type'],
        'description': selected.get('description', ''),
        'stats': selected.get('stats', {}),
        'effect': selected.get('effect', ''),
        'value': selected.get('value', 0)
    })
    print_success(f"Purchased {selected['name']}!")

def sell_item(player):
    if not player['inventory']:
        print_error("No items to sell!")
        return
    
    show_inventory(player)
    try:
        choice = int(input(f"Select item to sell (0 to cancel): {Fore.YELLOW}"))
        print(Style.RESET_ALL, end="")
        if choice == 0: return
        item = player['inventory'].pop(choice-1)
    except:
        print_error("Invalid choice!")
        return
    
    is_street_sale = random.random() < STREET_SALE_CHANCE
    price = calculate_sell_price(item, is_street_sale)
    
    if is_street_sale:
        print_info(f"Street sale! Price reduced to {price}")
    else:
        print_info(f"Sold for {price}")
    
    player['cash'] += price
    print_success(f"Added {price} cash!")

def atm_menu(player):
    while True:
        print_section("ATM")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} View Balance")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Deposit Cash")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Withdraw Cash")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Deposit Visa")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Withdraw Visa")
        print(f"{Fore.CYAN}6.{Style.RESET_ALL} Back")
        choice = input(f"Select option: {Fore.YELLOW}")
        print(Style.RESET_ALL, end="")
        
        if choice == '1':
            get_details(player)
        elif choice == '2':
            deposit_balance(player, 'cash')
        elif choice == '3':
            withdraw_balance(player, 'cash')
        elif choice == '4':
            deposit_balance(player, 'visa')
        elif choice == '5':
            withdraw_balance(player, 'visa')
        elif choice == '6':
            break
        else:
            print_error("Invalid option!")

def create_new_player():
    """Create a new player with starting values"""
    return {
        'name': input(f"Enter name: {Fore.YELLOW}"),
        'type': input(f"Enter character type: {Fore.YELLOW}"),
        'nickname': input(f"Choose nickname: {Fore.YELLOW}"),
        'cash': STARTING_CASH,
        'visa': STARTING_VISA,
        'inventory': [],
        'shops': [],
        'displayed_items': [],  # Items currently on display
        'last_customer_visit': None,  # Timestamp of last customer visit
        'customer_visit_chance': 0.3,  # Base chance of customer visit
        'store_locations': []  # List of owned store locations
    }

def customize_store(player, store):
    """Customize store name and type with penalties"""
    location_data = next((loc for loc in load_store_locations() if loc['name'] == store['name']), None)
    if not location_data:
        print_error("Invalid store location!")
        return False
    
    print_section("Store Customization")
    print(f"Current Name: {store.get('custom_name', location_data['default_name'])}")
    print(f"Current Type: {store.get('custom_type', location_data['default_type'])}")
    print(f"Allowed Types: {', '.join(location_data['allowed_types'])}")
    
    # Calculate current penalties
    name_penalty = 0.1 if 'custom_name' in store else 0
    type_penalty = 0.15 if 'custom_type' in store else 0
    total_penalty = name_penalty + type_penalty
    
    print(f"\nCurrent Customer Visit Penalty: {total_penalty * 100}%")
    
    while True:
        print(f"\n{Fore.CYAN}1.{Style.RESET_ALL} Change Store Name")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Change Store Type")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Back")
        
        choice = input(f"Select option: {Fore.YELLOW}")
        print(Style.RESET_ALL, end="")
        
        if choice == '1':
            new_name = input(f"Enter new store name (leave empty to use default): {Fore.YELLOW}")
            print(Style.RESET_ALL, end="")
            
            if new_name:
                store['custom_name'] = new_name
                print_success(f"Store name changed to {new_name}!")
                print_warning("This will reduce customer visits by 10%")
            else:
                if 'custom_name' in store:
                    del store['custom_name']
                    print_success("Store name reset to default!")
        
        elif choice == '2':
            print("\nAvailable Types:")
            for idx, type_name in enumerate(location_data['allowed_types'], 1):
                print(f"{Fore.CYAN}{idx}. {type_name}{Style.RESET_ALL}")
            
            try:
                type_choice = int(input(f"Select new type (0 to use default): {Fore.YELLOW}"))
                print(Style.RESET_ALL, end="")
                
                if type_choice == 0:
                    if 'custom_type' in store:
                        del store['custom_type']
                        print_success("Store type reset to default!")
                elif 1 <= type_choice <= len(location_data['allowed_types']):
                    new_type = location_data['allowed_types'][type_choice - 1]
                    store['custom_type'] = new_type
                    print_success(f"Store type changed to {new_type}!")
                    print_warning("This will reduce customer visits by 15%")
                else:
                    print_error("Invalid type choice!")
            except:
                print_error("Invalid input!")
        
        elif choice == '3':
            break
        else:
            print_error("Invalid option!")
    
    return True

def calculate_store_penalties(store):
    """Calculate total penalties for a store"""
    name_penalty = 0.1 if 'custom_name' in store else 0
    type_penalty = 0.15 if 'custom_type' in store else 0
    return name_penalty + type_penalty

def get_store_display_name(store):
    """Get the display name of a store (custom or default)"""
    location_data = next((loc for loc in load_store_locations() if loc['name'] == store['name']), None)
    return store.get('custom_name', location_data['default_name'])

def get_store_type(store):
    """Get the type of a store (custom or default)"""
    location_data = next((loc for loc in load_store_locations() if loc['name'] == store['name']), None)
    return store.get('custom_type', location_data['default_type'])

def buy_store(player, location):
    """Buy a store at a specific location"""
    store_locations = load_store_locations()
    location_data = next((loc for loc in store_locations if loc['name'] == location), None)
    
    if not location_data:
        print_error("Invalid location!")
        return False
    
    if location in [s['name'] for s in player['store_locations']]:
        print_error("You already own a store at this location!")
        return False
    
    if player['cash'] < location_data['price']:
        print_error(f"Not enough cash to buy a store! You need {location_data['price']} cash.")
        return False
    
    player['cash'] -= location_data['price']
    player['store_locations'].append({
        'name': location,
        'customer_visit_chance': location_data['customer_visit_chance'],
        'price_multiplier': location_data['price_multiplier'],
        'max_display_items': location_data['max_display_items'],
        'displayed_items': []
    })
    print_success(f"Successfully purchased store at {location}!")
    print_info(f"Description: {location_data['description']}")
    
    # Offer customization after purchase
    if input(f"Would you like to customize your new store? (y/n): {Fore.YELLOW}").lower() == 'y':
        print(Style.RESET_ALL, end="")
        customize_store(player, player['store_locations'][-1])
    
    return True

def display_item(player, item_index, location):
    """Display an item in the store at a specific location"""
    if item_index < 0 or item_index >= len(player['inventory']):
        print_error("Invalid item index!")
        return False
    
    store = next((s for s in player['store_locations'] if s['name'] == location), None)
    if not store:
        print_error("Invalid store location!")
        return False
    
    if len(store['displayed_items']) >= store['max_display_items']:
        print_error(f"Maximum number of displayed items ({store['max_display_items']}) reached!")
        return False
    
    item = player['inventory'].pop(item_index)
    location_data = next((loc for loc in load_store_locations() if loc['name'] == location), None)
    
    # Calculate base price
    base_price = int(item['value'] * store['price_multiplier'])
    
    # Allow player to set custom price
    print_info(f"Base price for this item: {base_price}")
    print_info("Price tiers and their sale chances:")
    for tier, data in location_data['price_tiers'].items():
        print(f"{tier.capitalize()}: Up to {data['max_price']} - Sale chance: {data['sale_chance'] * 100}%")
    
    try:
        custom_price = int(input(f"Enter custom price (0 to use base price): {Fore.YELLOW}"))
        print(Style.RESET_ALL, end="")
        if custom_price > 0:
            base_price = custom_price
    except:
        print_error("Invalid price! Using base price.")
    
    store['displayed_items'].append({
        'item': item,
        'display_time': datetime.now().timestamp(),
        'base_price': base_price,
        'days_on_display': 0
    })
    print_success(f"Item {item['name']} is now on display at {location} for {base_price} cash!")
    return True

def remove_displayed_item(player, item_index, location):
    """Remove an item from display at a specific location"""
    store = next((s for s in player['store_locations'] if s['name'] == location), None)
    if not store:
        print_error("Invalid store location!")
        return False
    
    if item_index < 0 or item_index >= len(store['displayed_items']):
        print_error("Invalid item index!")
        return False
    
    displayed = store['displayed_items'].pop(item_index)
    player['inventory'].append(displayed['item'])
    print_success(f"Item {displayed['item']['name']} removed from display at {location}!")
    return True

def check_customer_visit(player):
    """Check if a customer visits and potentially buys an item"""
    current_time = datetime.now().timestamp()
    
    for store in player['store_locations']:
        location_data = next((loc for loc in load_store_locations() if loc['name'] == store['name']), None)
        if not location_data:
            continue
        
        # Calculate time since last visit (in days)
        if 'last_customer_visit' in store:
            time_since_last = (current_time - store['last_customer_visit']) / (24 * 3600)  # Convert to days
            time_bonus = min(time_since_last / 180, 1.0)  # Max bonus after 180 days (6 months)
        else:
            time_bonus = 0
        
        # Calculate total chance with penalties
        base_chance = store['customer_visit_chance']
        penalties = calculate_store_penalties(store)
        total_chance = (base_chance - penalties) * (1 + time_bonus * 0.2)  # Reduced bonus to 20%
        
        if random.random() < total_chance:
            store['last_customer_visit'] = current_time
            
            if store['displayed_items']:
                # Update days on display for all items
                for displayed in store['displayed_items']:
                    displayed['days_on_display'] += 1
                
                # Calculate sale chances based on price tiers and time
                valid_items = []
                for displayed in store['displayed_items']:
                    price = displayed['base_price']
                    days = displayed['days_on_display']
                    
                    # Find the appropriate price tier
                    sale_chance = 0
                    for tier, data in location_data['price_tiers'].items():
                        if price <= data['max_price']:
                            sale_chance = data['sale_chance']
                            break
                    
                    # Increase chance based on days on display (max 365 days)
                    days_bonus = min(days / 365, 1.0) * 0.5  # Reduced to 50% bonus after 1 year
                    final_chance = sale_chance * (1 + days_bonus)
                    
                    if random.random() < final_chance:
                        valid_items.append(displayed)
                
                if valid_items:
                    # Customer buys a random item from valid items
                    item_index = random.randint(0, len(valid_items) - 1)
                    displayed = valid_items[item_index]
                    
                    # Calculate final price with minimal variation
                    price_variation = random.uniform(0.95, 1.05)  # Very small variation
                    final_price = int(displayed['base_price'] * price_variation)
                    
                    player['cash'] += final_price
                    store['displayed_items'].remove(displayed)
                    
                    store_name = get_store_display_name(store)
                    print_success(f"A customer bought {displayed['item']['name']} from your {store_name} store for {final_price} cash!")
                    print_info(f"The item was on display for {displayed['days_on_display']} days.")
                    return True
    
    return False

def store_management_menu(player):
    """Manage store operations"""
    while True:
        print_section("Store Management")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} View My Stores")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Buy New Store")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Manage Store Items")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Customize Store")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Back")
        
        choice = input(f"Select option: {Fore.YELLOW}")
        print(Style.RESET_ALL, end="")
        
        if choice == '1':
            if not player['store_locations']:
                print_info("You don't own any stores yet.")
            else:
                for store in player['store_locations']:
                    store_name = get_store_display_name(store)
                    store_type = get_store_type(store)
                    penalties = calculate_store_penalties(store)
                    
                    print(f"\n{Fore.CYAN}Store: {store_name}{Style.RESET_ALL}")
                    print(f"Type: {store_type}")
                    print(f"Location: {store['name']}")
                    print(f"Displayed Items: {len(store['displayed_items'])}/{store['max_display_items']}")
                    print(f"Base Customer Visit Chance: {store['customer_visit_chance'] * 100}%")
                    print(f"Current Penalties: {penalties * 100}%")
                    print(f"Effective Visit Chance: {(store['customer_visit_chance'] - penalties) * 100}%")
                    print(f"Price Multiplier: {store['price_multiplier']}x")
                    
                    if store['displayed_items']:
                        print("\nDisplayed Items:")
                        for idx, displayed in enumerate(store['displayed_items'], 1):
                            print(f"{Fore.CYAN}{idx}. {displayed['item']['name']} - Price: {displayed['base_price']}{Style.RESET_ALL}")
        
        elif choice == '2':
            store_locations = load_store_locations()
            available_locations = [loc for loc in store_locations 
                                if loc['name'] not in [s['name'] for s in player['store_locations']]]
            
            if not available_locations:
                print_error("No more store locations available!")
                continue
                
            print_section("Available Locations")
            for idx, loc in enumerate(available_locations, 1):
                print(f"\n{Fore.CYAN}{idx}. {loc['name']}{Style.RESET_ALL}")
                print(f"Default Name: {loc['default_name']}")
                print(f"Default Type: {loc['default_type']}")
                print(f"Allowed Types: {', '.join(loc['allowed_types'])}")
                print(f"Price: {loc['price']} cash")
                print(f"Description: {loc['description']}")
                print(f"Customer Visit Chance: {loc['customer_visit_chance'] * 100}%")
                print(f"Price Multiplier: {loc['price_multiplier']}x")
                print(f"Max Display Items: {loc['max_display_items']}")
                
            try:
                loc_choice = int(input(f"Select location to buy (0 to cancel): {Fore.YELLOW}"))
                print(Style.RESET_ALL, end="")
                if loc_choice == 0: continue
                buy_store(player, available_locations[loc_choice - 1]['name'])
            except:
                print_error("Invalid choice!")
        
        elif choice == '3':
            if not player['store_locations']:
                print_info("You don't own any stores yet.")
                continue
                
            print_section("Select Store")
            for idx, store in enumerate(player['store_locations'], 1):
                print(f"{Fore.CYAN}{idx}. {get_store_display_name(store)}{Style.RESET_ALL}")
                
            try:
                store_choice = int(input(f"Select store to manage (0 to cancel): {Fore.YELLOW}"))
                print(Style.RESET_ALL, end="")
                if store_choice == 0: continue
                selected_store = player['store_locations'][store_choice - 1]
                
                while True:
                    print_section(f"Managing {get_store_display_name(selected_store)}")
                    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Display New Item")
                    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Remove Displayed Item")
                    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Back")
                    
                    sub_choice = input(f"Select option: {Fore.YELLOW}")
                    print(Style.RESET_ALL, end="")
                    
                    if sub_choice == '1':
                        show_inventory(player)
                        try:
                            item_choice = int(input(f"Select item to display (0 to cancel): {Fore.YELLOW}"))
                            print(Style.RESET_ALL, end="")
                            if item_choice == 0: continue
                            display_item(player, item_choice - 1, selected_store['name'])
                        except:
                            print_error("Invalid choice!")
                    
                    elif sub_choice == '2':
                        if not selected_store['displayed_items']:
                            print_info("No items on display.")
                            continue
                            
                        for idx, displayed in enumerate(selected_store['displayed_items'], 1):
                            print(f"{Fore.CYAN}{idx}. {displayed['item']['name']} - Price: {displayed['base_price']}{Style.RESET_ALL}")
                            
                        try:
                            item_choice = int(input(f"Select item to remove (0 to cancel): {Fore.YELLOW}"))
                            print(Style.RESET_ALL, end="")
                            if item_choice == 0: continue
                            remove_displayed_item(player, item_choice - 1, selected_store['name'])
                        except:
                            print_error("Invalid choice!")
                    
                    elif sub_choice == '3':
                        break
                    else:
                        print_error("Invalid option!")
                        
                    check_customer_visit(player)
            except:
                print_error("Invalid choice!")
        
        elif choice == '4':
            if not player['store_locations']:
                print_info("You don't own any stores yet.")
                continue
                
            print_section("Select Store to Customize")
            for idx, store in enumerate(player['store_locations'], 1):
                print(f"{Fore.CYAN}{idx}. {get_store_display_name(store)}{Style.RESET_ALL}")
                
            try:
                store_choice = int(input(f"Select store to customize (0 to cancel): {Fore.YELLOW}"))
                print(Style.RESET_ALL, end="")
                if store_choice == 0: continue
                customize_store(player, player['store_locations'][store_choice - 1])
            except:
                print_error("Invalid choice!")
        
        elif choice == '5':
            break
        else:
            print_error("Invalid option!")
            
        check_customer_visit(player) 