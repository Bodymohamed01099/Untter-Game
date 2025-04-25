Here's a well-structured `README.md` for your project:

# The Untter Game

## Overview

The Untter Game is an interactive simulation game where players manage their own stores, inventory, and finances. The game allows players to buy and sell items, manage customer visits, and track progress through a set of operations like depositing money, managing stores, and displaying items.

## Features

- **Game Management**: Create and manage players, stores, and inventory.
- **Data Management**: Save, load, backup, and delete game data.
- **Player Management**: Buy, sell, and view items in inventory.
- **ATM Management**: Deposit and withdraw money from accounts.
- **Store Management**: Set up and manage player-owned stores.
- **Customer Interactions**: Handle customer visits and manage inventory display.
  
## File Structure

```
The-Untter-Game/
├── Functions/
│   ├── CoreFunctions.py
│   ├── DataManagement.py
│   ├── Game/
│   │   ├── GameFunctions.py
│   │   ├── ATMFunctions.py
│   │   ├── GameFlow.py
│   │   └── GameUtils.py
└── README.md
```

## Core Functions (`Functions/CoreFunctions.py`)

### Display Functions

- `print_header()`: Displays the game's ASCII art title.
- `print_divider()`: Prints a yellow divider line for visual separation.
- `print_section(title)`: Displays a formatted section header with green text.
- `print_success(message)`: Displays success messages with a green checkmark.
- `print_error(message)`: Displays error messages with a red X.
- `print_info(message)`: Displays informational messages with a blue info symbol.
- `print_warning(message)`: Displays warning messages with a yellow warning symbol.

## Data Management Functions (`Functions/DataManagement.py`)

### Directory Management

- `ensure_directories()`: Creates necessary database directories if they don't exist.
- `load_data()`: Loads game data from a JSON file; creates new file if none exists.
- `load_stores()`: Loads store data from a JSON file; creates new file if none exists.
- `save_data(data)`: Saves game data to a JSON file.

### File Operations

- `list_saved_files()`: Lists all saved game files with details.
- `create_backup()`: Creates a backup of the current game data.
- `delete_save_file(filename)`: Deletes a specified save file.
- `export_game_data(player)`: Exports player data to a JSON file.
- `import_game_data()`: Imports player data from a JSON file.

### Menu Functions

- `file_management_menu(data)`: Displays and handles file management options.

## Game Functions (`Functions/Game/GameFunctions.py`)

### Player Management

- `show_inventory(player)`: Displays player's inventory items.
- `buy_from_store(player)`: Handles purchasing items from stores.
- `sell_item(player)`: Handles selling items from inventory.
- `create_new_player()`: Creates a new player with starting values.

### Store Functions

- `load_store_locations()`: Loads available store locations from JSON file.
- `store_management_menu(player)`: Manages player-owned stores.
- `check_customer_visit(player)`: Handles random customer visits to player stores.
- `display_item(player, item_index, location)`: Places an item on display at a store location.
- `remove_displayed_item(player, item_index, location)`: Removes an item from display.
- `calculate_store_penalties(store)`: Calculates penalties affecting customer visit chances.

### ATM Functions (`Functions/Game/ATMFunctions.py`)

- `get_details(player)`: Displays player's account details.
- `deposit_balance(player, account_type)`: Deposits money into specified account.
- `withdraw_balance(player, account_type)`: Withdraws money from specified account.
- `atm_menu(player)`: Displays and handles ATM operations.

## Game Flow (`Functions/Game/GameFlow.py`)

- `new_game(data)`: Starts a new game with player creation.
- `continue_game(data)`: Continues an existing game by loading player data.
- `game_loop(player, data)`: Main game loop with menu options.

## Game Utilities (`Functions/Game/GameUtils.py`)

### Constants

- `STARTING_CASH`: Initial cash amount (500).
- `STARTING_VISA`: Initial visa amount (200).
- `STREET_SALE_CHANCE`: Probability of street sale (0.3).
- `STREET_SALE_DISCOUNT`: Discount factor for street sales (0.7).

### Formatting Functions

- `format_item(item)`: Formats item details with appropriate colors.
- `calculate_sell_price(item, is_street_sale)`: Calculates selling price of items.
- `validate_amount(amount)`: Validates monetary amounts.

## Data Structures

### Player Object

- `name`: Player's full name.
- `type`: Character type or class.
- `nickname`: Player's chosen nickname.
- `cash`: Current cash on hand.
- `visa`: Current visa card balance.
- `inventory`: List of items owned by player.
- `shops`: List of shops owned by player.
- `store_locations`: List of store locations owned by player.
- `displayed_items`: Items currently on display in shops.
- `last_customer_visit`: Timestamp of last customer visit.
- `customer_visit_chance`: Base chance of customer visit.

### Item Object

- `name`: Name of the item.
- `value`: Base value of the item.
- `type`: Type of item (weapon, armor, consumable, etc.).
- `description`: Item description.
- `stats`: Object containing item statistics.
- `effect`: Special effect of the item.
- `price`: Purchase price in stores.

### Store Object

- `name`: Name of the store.
- `type`: Type of store (General, Luxury, etc.).
- `price`: Purchase cost of the store.
- `customer_visit_chance`: Probability of customer visits.
- `price_multiplier`: Affects selling prices.
- `description`: Store description.
- `max_display_items`: Maximum items that can be displayed.
- `daily_visitors`: Average number of daily visitors.
- `allowed_types`: Types of items that can be sold.
- `price_tiers`: Different price categories with sale chances.
- `displayed_items`: Array of items currently on display with metadata.
- `last_customer_visit`: Timestamp tracking when customers last visited.

### Displayed Item Object

- `item`: The actual item object being displayed.
- `display_time`: Timestamp when the item was put on display.
- `base_price`: The price set by the player.
- `days_on_display`: Number of days the item has been on display.

## Installation

To install the game, simply clone this repository:

```bash
git clone https://github.com/yourusername/The-Untter-Game.git
```

Then, navigate into the project folder:

```bash
cd The-Untter-Game
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the game by executing the following command:

```bash
python main.py
```

Follow the on-screen instructions to create your player, manage your stores, and interact with the world.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
