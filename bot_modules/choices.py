# bot_modules/choices.py
import discord.app_commands as app_commands

from bot_modules import constants

# Define the roles for Tank, Healer, and DPS using emoji symbols
role_emojis = {
    "Tank": "<:wow_tank:868737094242152488>",
    "Healer": "<:wow_healer:868737094258950144>",
    "DPS": "<:wow_dps:868737094011486229>",
    "Clear Role": "❌"  
}

dungeon_choices = [
    app_commands.Choice(name="Ara-Kara, City of Echoes", value="ara"),
    app_commands.Choice(name="City of Threads", value="cot"),
    app_commands.Choice(name="The Stonevault", value="vault"),
    app_commands.Choice(name="The Dawnbreaker", value="dawnbreaker"),
    app_commands.Choice(name="Mists of Tirna Scithe", value="mists"),
    app_commands.Choice(name="The Necrotic Wake", value="necrotic wake"),
    app_commands.Choice(name="Siege of Boralus", value="siege"),
    app_commands.Choice(name="Any", value="any"),
    app_commands.Choice(name="Grim Batol", value="grim"),
    app_commands.Choice(name="Any", value="Any")
]

difficulty_choices = [
    app_commands.Choice(name="Normal", value="Normal"),
    app_commands.Choice(name="Heroic", value="Heroic"),
    app_commands.Choice(name="Mythic", value="Mythic"),
    app_commands.Choice(name="Delve", value="Delve")
]

role_choices = [
    app_commands.Choice(name="Healer", value=f"healer{role_emojis['Healer']}"),
    app_commands.Choice(name="Tank", value=f"tank{role_emojis['Tank']}"),
    app_commands.Choice(name="DPS", value=f"dps{role_emojis['DPS']}"),
]

yes_no_choices = [
    app_commands.Choice(name="yes", value="yes"),
    app_commands.Choice(name="no", value="no")
]

level_choices = [
    app_commands.Choice(name="0", value="0"),
    app_commands.Choice(name="2", value="2"),
    app_commands.Choice(name="3", value="3"),
    app_commands.Choice(name="4", value="4"),
    app_commands.Choice(name="5", value="5"),
    app_commands.Choice(name="6", value="6"),
    app_commands.Choice(name="7", value="7"),
    app_commands.Choice(name="8", value="8"),
    app_commands.Choice(name="9", value="9"),
    app_commands.Choice(name="10", value="10"),
    app_commands.Choice(name="11", value="11"),
    app_commands.Choice(name="12", value="12"),
    app_commands.Choice(name="13", value="13"),
    app_commands.Choice(name="14", value="14"),
    app_commands.Choice(name="15", value="15"),
    app_commands.Choice(name="16", value="16"),
    app_commands.Choice(name="17", value="17"),
    app_commands.Choice(name="18", value="18"),
    app_commands.Choice(name="19", value="19"),
    app_commands.Choice(name="20", value="20"),
    app_commands.Choice(name="N/A", value="N/A"),
]

prod_mention_choices = {
  "healer_role": "<@&1281359918330413190>",
  "tank_role": "<@&1281359855885750372>",
  "dps_role": "<@&1281359999662034945>",
  "normal_role":"<@&1281360125419978856>",
  "heroic_role":"<@&1281360082726162560>",
  "mythic_role":" <@&1281360042117042247>",
  "delve_role": "<@&1281360167778123958>"
}

dev_mention_choices = {
  "healer_role": "<@&1281358200104423529>",
  "tank_role": "<@&1281358460079833161>",
  "dps_role": "<@&1281358602610937959>",
  "normal_role":"<@&1281358751252877385>",
  "heroic_role":"<@&1281358691915923517>",
  "mythic_role":"<@&1281358645400965180>",
  "delve_role": "<@&1281358894014398558>"
}

def mention_helper(server_id: str, role: str = None, difficulty: str = None):
    # Determine the mention choices based on the server ID
    if server_id in constants.SG_DEV_SERVER_ID:
        mention_choices = dev_mention_choices
    elif server_id in constants.SG_PROD_SERVER_ID:
        mention_choices = prod_mention_choices
    else:
        return None
    
    # Filter mention choices based on role and difficulty
    filtered_mentions = {}

    if role:
        role_mention = mention_choices.get(f"{role}_role")
        if role_mention:
            filtered_mentions["role"] = role_mention

    if difficulty:
        difficulty_mention = mention_choices.get(f"{difficulty}_role")
        if difficulty_mention:
            filtered_mentions["difficulty"] = difficulty_mention

    return filtered_mentions