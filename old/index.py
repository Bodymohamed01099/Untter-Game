def get_details(name,  balance, bank_balance):
    print(f"Name: {name}")
    print(f"Balance: ${balance}")
    print(f"Bank Balance: ${bank_balance}")

def deposit_balance(balance, bank_balance):
    amount = float(input("Enter deposit amount: $"))

    if (amount > balance):
        print("Error: Insufficient funds.")
    elif amount <= 0:
        print("Error: Amount must be greater than 0.")
    else:
        balance += amount
        print(f"Deposit successful! New balance: ${balance}")
    return balance

def withdraw_balance(balance, bank_balance):
    amount = float(input("Enter withdrawal amount: $"))
    
    if (amount > balance):
        print("Error: Insufficient funds.")
    elif amount <= 0:
        print("Error: Amount must be greater than 0.")
    else:
        balance -= amount
        print(f"Withdrawal successful! New balance: ${balance}")
    return balance

def main():
    name = input("Enter your name: ")
    balance = float(input("Enter your Wallet balance: $"))
    bank_balance = float(input("Enter your Bank balance: $"))
    
    while True:
        print("\nChoose an option:")
        print("1. Get Details")
        print("2. Deposit Balance")
        print("3. Withdraw Balance")
        
        choice = input("Enter choice (1, 2, or 3): ")
        
        if choice == '1':
            get_details(name, balance, bank_balance)
        elif choice == '2':
            balance = deposit_balance(balance, bank_balance)
        elif choice == '3':
            balance = withdraw_balance(balance, bank_balance)
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
        
        cont = input("Do you want to perform another action? (y/n): ")
        if cont.lower() != 'y':
            print("Exiting program.")
            break

main()
