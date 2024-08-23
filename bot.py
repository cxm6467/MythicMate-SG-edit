import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
import os
from dotenv import load_dotenv

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

# Define the roles for Tank, Healer, and DPS using emoji symbols
role_emojis = {
    "Tank": "🛡️",
    "Healer": "💚",
    "DPS": "⚔️",
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
    app_commands.Choice(name="Grim Batol", value="grim")
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

key_level_choices = [app_commands.Choice(name=str(i), value=str(i)) for i in range(2, 31)]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()  # Synchronize the command tree with Discord
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")


# Define the modal for the slash command
class LFMModal(ui.Modal):
    def __init__(self, interaction: discord.Interaction, dungeon: str = '', key_level: str = '', role: str = '', res: str = '', lust: str = '', title="Looking for Members"):
        super().__init__(title=title)
        
        # Set up text inputs with defaults provided
        self.dungeon_input = ui.TextInput(
            label="Dungeon Name", 
            placeholder="Enter dungeon name", 
            default=dungeon,  # Set default directly
            required=True
        )

        self.key_level_input = ui.TextInput(
            label="Key Level", 
            placeholder="Enter key level (e.g., +10)", 
            default=key_level,  # Set default directly
            required=True
        )
        self.role_input = ui.TextInput(
            label="Role", 
            placeholder="Enter your role (e.g., Tank, Healer, DPS)", 
            default=role,  # Set default directly
            required=True
        )

        self.res_input = ui.TextInput(
            label="Res",
            placeholder='Enter yes or no if you have a battle res',
            default=res,  # Set default directly
            required=True
        )

        self.lust_input = ui.TextInput(
            label="Lust",
            placeholder='Enter yes or no if you have a bloodlust-like ability',
            default=lust,  # Set default directly
            required=True
        )
        
        self.add_item(self.dungeon_input)
        self.add_item(self.key_level_input)
        self.add_item(self.role_input)
        self.add_item(self.res_input)
        self.add_item(self.lust_input)

        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        # Defer the interaction to prevent timeout errors
        await interaction.response.defer()

        dungeon = self.dungeon_input.value
        key_level = self.key_level_input.value
        role = self.role_input.value
        res = self.res_input.value
        lust = self.lust_input.value

        # Create an embed message to display the group information
        embed = discord.Embed(
            title=f"Dungeon: {dungeon}",
            description=f"Difficulty: {key_level}",
            color=discord.Color.blue()
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

        # Initialize members based on the role the user selected
        if role.lower() == "tank":
            members = {"Tank": interaction.user, "Healer": None, "DPS": []}
        elif role.lower() == "healer":
            members = {"Tank": None, "Healer": interaction.user, "DPS": []}
        elif role.lower() == "dps":
            members = {"Tank": None, "Healer": None, "DPS": [interaction.user]}
        else:
            members = {"Tank": None, "Healer": None, "DPS": []}

        # Populate the embed with initial values for Tank, Healer, and DPS roles
        embed.add_field(name="🛡️ Tank", value=members["Tank"].mention if members["Tank"] else "None", inline=False)
        embed.add_field(name="💚 Healer", value=members["Healer"].mention if members["Healer"] else "None", inline=False)

        # Add one field for DPS with placeholders for up to three DPS members
        dps_value = "\n".join([dps_user.mention for dps_user in members["DPS"]] + ["None"] * (3 - len(members["DPS"])))
        embed.add_field(name="⚔️ DPS", value=dps_value, inline=False)

        # Send the embed message as a follow-up to the deferred response
        group_message = await interaction.followup.send(embed=embed)

        # Add reaction emojis for Tank, Healer, DPS, and Clear Role
        for emoji in role_emojis.values():
            await group_message.add_reaction(emoji)
        
                # Create a thread for this group message
        # Create a thread for this group message using the channel
        await interaction.channel.create_thread(
            name=f"Group for {dungeon} +{key_level}",
            message=group_message,  # Attach the thread to the group message
            auto_archive_duration=1440,  # Auto-archive after 24 hours of inactivity
            reason="Starting group thread for dungeon run"
        )

# Slash command to invoke the modal
@bot.tree.command(name="lfm", description="Start looking for members for a Mythic+ run.")
@app_commands.describe(dungeon='Choose a dungeon', key_level='Enter the key level', role="Enter your role", res="Do you bring a battle res?", lust="Do you bring a lust?")
@app_commands.choices(dungeon=dungeon_choices)
@app_commands.choices(key_level=key_level_choices)
@app_commands.choices(role=role_choices)
@app_commands.choices(res=yes_no_choices)
@app_commands.choices(lust=yes_no_choices)
async def lfm(interaction: discord.Interaction, dungeon: str, key_level: str, role: str, res: str, lust: str):
    full_dungeon_name = translate_dungeon_name(dungeon)

    if not full_dungeon_name:
        await interaction.response.send_message(f"Sorry, I couldn't recognize the dungeon name '{dungeon}'. Please try again with a valid name or abbreviation.", ephemeral=True)
        return

    await interaction.response.send_modal(LFMModal(interaction, full_dungeon_name, key_level, role, res, lust))

# Run the bot with the token loaded from the environment variables
bot.run(TOKEN)
