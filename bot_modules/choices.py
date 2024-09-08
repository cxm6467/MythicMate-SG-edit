# bot_modules/choices.py
import discord.app_commands as app_commands
import discord

# Define the roles for Tank, Healer, and DPS using emoji symbols
role_emojis = {
    "Tank": "<:wow_tank:868737094242152488>",
    "Healer": "<:wow_healer:868737094258950144>",
    "DPS": "<:wow_dps:868737094011486229>",
    "Clear Role": "❌"  
}

dungeon_choices = [
    app_commands.Choice(name="Any", value="any"),
    app_commands.Choice(name="Ara-Kara, City of Echoes", value="ara"),
    app_commands.Choice(name="City of Threads", value="cot"),
    app_commands.Choice(name="The Stonevault", value="vault"),
    app_commands.Choice(name="The Dawnbreaker", value="dawnbreaker"),
    app_commands.Choice(name="Mists of Tirna Scithe", value="mists"),
    app_commands.Choice(name="The Necrotic Wake", value="necrotic wake"),
    app_commands.Choice(name="Siege of Boralus", value="siege"),
    app_commands.Choice(name="Grim Batol", value="grim")
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
meridiem_choices = [
    discord.SelectOption(label="12", value="12"),
    discord.SelectOption(label="24", value="24", default=True)
]

tz_options = [
    discord.SelectOption(label="Eastern Standard Time (EST)", value="EST", default=True),
    discord.SelectOption(label="Central Standard Time (CST)", value="CST"),
    discord.SelectOption(label="Mountain Standard Time (MST)", value="MST"),
    discord.SelectOption(label="Pacific Standard Time (PST)", value="PST")
]