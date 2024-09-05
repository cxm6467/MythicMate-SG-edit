# bot_modules/choices.py
import discord.app_commands as app_commands

# Define the roles for Tank, Healer, and DPS using emoji symbols
role_emojis = {
    "Tank": "<:wow_tank:868737094242152488>",
    "Healer": "<:wow_healer:868737094258950144>",
    "DPS": "<:wow_dps:868737094011486229>",
    "Clear Role": "❌"  # This emoji is used to allow users to clear their selected role
}

dungeon_choices = [
    app_commands.Choice(name="Ara-Kara, City of Echoes", value="ara"),
    app_commands.Choice(name="City of Threads", value="cot"),
    app_commands.Choice(name="The Stonevault", value="vault"),
    app_commands.Choice(name="The Dawnbreaker", value="dawnbreaker"),
    app_commands.Choice(name="Mists of Tirna Scithe", value="mists"),
    app_commands.Choice(name="The Necrotic Wake", value="necrotic wake"),
    app_commands.Choice(name="Siege of Boralus", value="siege"),
    app_commands.Choice(name="Grim Batol", value="grim"),
    app_commands.Choice(name="Delve", value="Delve")
]

difficulty_choices = [
    app_commands.Choice(name="M+", value="M+"),
    app_commands.Choice(name="M0", value="M0"),
    app_commands.Choice(name="Normal", value="Normal"),
    app_commands.Choice(name="Heroic", value="Heroic"),
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