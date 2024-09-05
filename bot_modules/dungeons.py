# bot_modules/dungeons.py
import discord
from discord import app_commands
from typing import List

# Define the available dungeons and their abbreviations
dungeon_aliases = {
    "Ara-Kara, City of Echoes": ["ara", "city of echoes", "coe"],
    "City of Threads": ["threads", "city of threads", "cot"],
    "The Stonevault": ["stonevault", "vault"],
    "The Dawnbreaker": ["dawnbreaker", "breaker"],
    "Mists of Tirna Scithe": ["mists", "tirna", "scithe", "mots"],
    "The Necrotic Wake": ["nw", "necrotic wake", "necrotic"],
    "Siege of Boralus": ["siege", "boralus", "sob"],
    "Grim Batol": ["grim", "batol", "gb"],
    "Any": ["Any", "any"]
}

# Define the available dungeons and their abbreviations
dungeon_urls = {
    "Ara-Kara, City of Echoes": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-kikatal.png",
    "City of Threads": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-izo.png",
    "The Stonevault": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-eirich.png",
    "The Dawnbreaker": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-rashanan.png",
    "Mists of Tirna Scithe": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-mistcaller.png",
    "The Necrotic Wake": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-nalthortherimebinder.png",
    "Siege of Boralus": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-viqgoth.png",
    "Grim Batol": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-erudax-updated.png",
    "Any":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/WoW_icon.svg/48px-WoW_icon.svg.png?20171015201105",
}

# Function to translate user input to the full dungeon name
def translate_dungeon_name(user_input):
    user_input = user_input.lower()
    for full_name, aliases in dungeon_aliases.items():
        if user_input in aliases or user_input == full_name.lower():
            return full_name
    return None

async def level_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    # Define the special values and the numeric range
    special_values = ['0', 'N/A']
    numeric_values = [str(i) for i in range(2, 31)]
    
    # Combine all values
    all_values = special_values + numeric_values

    # Debug print statement
    print(f"Debug: current='{current}', all_values={all_values}")

    # Return only those values that contain the current input
    choices = [
        app_commands.Choice(name=value, value=value)
        for value in all_values if current.lower() in value.lower()
    ]
    
    # Debug print statement for choices
    print(f"Debug: choices={choices}")
    
    return choices