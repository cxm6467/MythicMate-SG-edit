# bot_modules/dungeons.py

# Define the available dungeons and their abbreviations
dungeon_aliases = {
    "Ara-Kara, City of Echoes": ["ara", "city of echoes", "coe"],
    "City of Threads": ["threads", "city of threads", "cot"],
    "The Stonevault": ["stonevault", "vault"],
    "The Dawnbreaker": ["dawnbreaker", "breaker"],
    "Mists of Tirna Scithe": ["mists", "tirna", "scithe", "mots"],
    "The Necrotic Wake": ["nw", "necrotic wake", "necrotic"],
    "Siege of Boralus": ["siege", "boralus", "sob"],
    "Grim Batol": ["grim", "batol", "gb"]
}

# Function to translate user input to the full dungeon name
def translate_dungeon_name(user_input):
    user_input = user_input.lower()
    for full_name, aliases in dungeon_aliases.items():
        if user_input in aliases or user_input == full_name.lower():
            return full_name
    return None
