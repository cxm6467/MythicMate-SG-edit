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
    "Grim Batol": ["grim", "batol", "gb"],
    "Delve": ["Delve", "delve"]
}

# Define the available dungeons and their abbreviations
# Define the available dungeons and their abbreviations as a single string
dungeon_urls = {
    "Ara-Kara, City of Echoes": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-kikatal.png",
    "City of Threads": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-izo.png",
    "The Stonevault": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-eirich.png",
    "The Dawnbreaker": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-rashanan.png",
    "Mists of Tirna Scithe": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-mistcaller.png",
    "The Necrotic Wake": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-nalthortherimebinder.png",
    "Siege of Boralus": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-viqgoth.png",
    "Grim Batol": "https://wow.zamimg.com/images/wow/journal/ui-ej-boss-erudax-updated.png",
    "Delve":"https://wow.zamimg.com/uploads/screenshots/small/1170483.jpg"
}

# Function to translate user input to the full dungeon name
def translate_dungeon_name(user_input):
    user_input = user_input.lower()
    for full_name, aliases in dungeon_aliases.items():
        if user_input in aliases or user_input == full_name.lower():
            return full_name
    return None
