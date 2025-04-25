from colorama import Fore, Style

STARTING_CASH = 500
STARTING_VISA = 200
STREET_SALE_CHANCE = 0.3
STREET_SALE_DISCOUNT = 0.7

ITEM_TYPES = {
    'weapon': Fore.RED,
    'armor': Fore.BLUE,
    'consumable': Fore.GREEN,
    'magic': Fore.MAGENTA
}

STAT_COLORS = {
    'attack': Fore.RED,
    'defense': Fore.BLUE,
    'durability': Fore.YELLOW,
    'speed': Fore.CYAN,
    'mana': Fore.MAGENTA
}

EFFECT_COLORS = {
    'heal': Fore.GREEN,
    'damage': Fore.RED,
    'mana': Fore.MAGENTA,
    'fire': Fore.RED,
    'ice': Fore.CYAN,
    'lightning': Fore.YELLOW
}

def format_item(item):
    """Format item details with appropriate colors"""
    color = Fore.CYAN
    if item['type'] == 'weapon':
        color = Fore.RED
    elif item['type'] == 'armor':
        color = Fore.GREEN
    elif item['type'] == 'consumable':
        color = Fore.YELLOW
    elif item['type'] == 'magic':
        color = Fore.MAGENTA
    
    output = []
    output.append(f"{color}{item['name']} - Value: {item.get('value', item.get('price', 0))}{Style.RESET_ALL}")
    
    if 'description' in item:
        output.append(f"   Description: {item['description']}")
    
    if 'stats' in item:
        for stat, value in item['stats'].items():
            output.append(f"   {stat.capitalize()}: {value}")
    
    if 'effect' in item:
        output.append(f"   Effect: {item['effect']} - Value: {item.get('value', 0)}")
    
    return '\n'.join(output)

def calculate_sell_price(item, is_street_sale=False):
    """Calculate the selling price of an item based on its stats and type"""
    base_value = 0
    
    # Calculate base value from stats
    if 'stats' in item:
        for stat, value in item['stats'].items():
            if stat == 'attack':
                base_value += value * 10
            elif stat == 'defense':
                base_value += value * 8
            elif stat == 'durability':
                base_value += value * 5
            elif stat == 'speed':
                base_value += value * 7
            elif stat == 'mana':
                base_value += value * 6
    
    # Add value for effects
    if 'effect' in item and item['effect']:
        base_value += 50  # Base value for having an effect
        if 'power' in item['effect']:
            base_value += item['effect']['power'] * 5
    
    # Apply type multiplier
    type_multiplier = 1.0
    if item['type'] == 'weapon':
        type_multiplier = 1.2
    elif item['type'] == 'armor':
        type_multiplier = 1.1
    elif item['type'] == 'magic':
        type_multiplier = 1.3
    
    # Calculate final value
    final_value = int(base_value * type_multiplier)
    
    # Apply street sale discount if applicable
    if is_street_sale:
        final_value = int(final_value * STREET_SALE_DISCOUNT)
    
    return final_value

def validate_amount(amount):
    """Validate a monetary amount"""
    try:
        amount = float(amount)
        if amount <= 0:
            return False
        return True
    except:
        return False 