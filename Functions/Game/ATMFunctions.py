from colorama import Fore, Style
from Functions.CoreFunctions import print_section, print_success, print_error, print_info
from Functions.Game.GameUtils import validate_amount

# ATM functions
def get_details(player):
    """Display player's account details"""
    print_section("Player Details")
    print(f"{Fore.CYAN}Name:{Style.RESET_ALL} {player['name']}")
    print(f"{Fore.GREEN}Cash Balance:{Style.RESET_ALL} {player['cash']}")
    print(f"{Fore.BLUE}Visa Balance:{Style.RESET_ALL} {player['visa']}")

def deposit_balance(player, account_type):
    """Deposit money into player's account"""
    try:
        amount = float(input(f"Enter amount to deposit: {Fore.YELLOW}"))
        print(Style.RESET_ALL, end="")
        
        if not validate_amount(amount):
            return
            
        player[account_type] += amount
        print_success(f"Deposited {amount} to {account_type}. New balance: {player[account_type]}")
    except ValueError:
        print_error("Invalid input!")

def withdraw_balance(player, account_type):
    """Withdraw money from player's account"""
    try:
        amount = float(input(f"Enter amount to withdraw: {Fore.YELLOW}"))
        print(Style.RESET_ALL, end="")
        
        if not validate_amount(amount):
            return
            
        if player[account_type] < amount:
            print_error("Insufficient funds!")
            return
            
        player[account_type] -= amount
        print_success(f"Withdrew {amount} from {account_type}. New balance: {player[account_type]}")
    except ValueError:
        print_error("Invalid input!")