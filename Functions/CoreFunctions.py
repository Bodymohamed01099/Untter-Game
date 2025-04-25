from colorama import Fore, Style

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

def print_error(message):
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}") 