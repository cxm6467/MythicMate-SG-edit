import discord
from discord.ext import commands 
from discord import app_commands
import os
from dotenv import load_dotenv 
import bot_modules.dungeons as dungeons  # Import dungeon-related data/functions
import bot_modules.choices as choices    # Import predefined choices
import bot_modules.modal as modal

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
TOKEN = os.getenv('BOT_TOKEN')

# Configure the bot with the necessary intents (permissions)
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True

# Initialize the bot with a command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # Ensure command syncing with Discord
    try:
        await bot.tree.sync()  # Synchronize the command tree with Discord
    except Exception as e:
        print(f"Error syncing commands: {e}")


# Slash command to invoke the modal
@bot.tree.command(name="lfm", description="Start looking for members for a dungeon run.")
@app_commands.describe(difficulty="Choose a dungeon difficulty", dungeon='Choose a dungeon', key_level='Enter the key level or N/A', role="Enter your role", res="Do you bring a battle res?", lust="Do you bring a lust?")
@app_commands.choices(difficulty=choices.difficulty_choices)
@app_commands.choices(dungeon=choices.dungeon_choices)
@app_commands.choices(role=choices.role_choices)
@app_commands.choices(res=choices.yes_no_choices)
@app_commands.choices(lust=choices.yes_no_choices)
async def lfm(interaction: discord.Interaction, difficulty:str, dungeon: str, key_level: str, role: str, res: str = None, lust: str = None):
    full_dungeon_name = dungeons.translate_dungeon_name(dungeon)

    if not full_dungeon_name:
        await interaction.response.send_message(f"Sorry, I couldn't recognize the dungeon name '{dungeon}'. Please try again with a valid name or abbreviation.", ephemeral=True)
        return

    await interaction.response.send_modal(modal.LFMModal(interaction, difficulty, full_dungeon_name, key_level, role, res, lust))

# Run the bot with the token loaded from the environment variables
bot.run(TOKEN)
