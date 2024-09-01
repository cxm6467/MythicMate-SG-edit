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
    # Create members and a group message here
    full_dungeon_name = dungeons.translate_dungeon_name(dungeon)

    if not full_dungeon_name:
        await interaction.response.send_message(f"Sorry, I couldn't recognize the dungeon name '{dungeon}'. Please try again with a valid name or abbreviation.", ephemeral=True)
        return
    
    if "tank" in role.lower():
        members = {"Tank": interaction.user, "Healer": None, "DPS": []}
    elif "healer" in role.lower():
        members = {"Tank": None, "Healer": interaction.user, "DPS": []}
    elif "dps" in role.lower():
        members = {"Tank": None, "Healer": None, "DPS": [interaction.user]}
    else:
        members = {"Tank": None, "Healer": None, "DPS": []}
    
    # new embed
    blank_embed = discord.Embed(
        description="temp"
    )
    
    lfmModal = modal.LFMModal(interaction, difficulty, full_dungeon_name, key_level, role, res, lust, members, blank_embed)
    await interaction.response.send_modal(lfmModal)
    

    # Send the embed message as a follow-up to the deferred response
    group_message = await interaction.followup.send(embed=blank_embed)
        # Function to update the embed with the latest group information
        # Loop to wait for the "✅" reaction indicating the group is complete
            # Initialize members based on the role the user selected
            
    # Function to check if a reaction is valid and relevant to the current group message
    def check_reaction(reaction, user):
        return user != bot.user and reaction.message.id == group_message.id

        # Event handler for when a user adds a reaction to the group message
    @bot.event
    async def on_reaction_add(reaction, user):
        if reaction.message.id != group_message.id or user == bot.user:
            return

        # Handle the "Clear Role" reaction to remove a user's role
        if str(reaction.emoji) == choices.role_emojis["Clear Role"]:
            if user == members["Tank"]:
                members["Tank"] = None
            elif user == members["Healer"]:
                members["Healer"] = None
            elif user in members["DPS"]:
                members["DPS"].remove(user)

            # Remove the user's other role-related reactions
            for role, emoji in choices.role_emojis.items():
                if emoji != choices.role_emojis["Clear Role"]:
                    await group_message.remove_reaction(emoji, user)

            await update_embed()  # Update the embed with the cleared role
            await group_message.remove_reaction(reaction.emoji, user)
            return

        # Prevent users from selecting multiple roles
        if user in [members["Tank"], members["Healer"], *members["DPS"]]:
            await group_message.remove_reaction(reaction.emoji, user)
            await user.send("You can only select one role.")
            return
        
        # Initialize the members dictionary based on the role the user selected
        member_reactions = {"Tank": None, "Healer": None, "DPS": []}
        
        # Assign the user to the selected role based on their reaction
        if str(reaction.emoji) == choices.role_emojis["Tank"] and not members["Tank"]:
            members["Tank"] = user
            member_reactions["Tank"] = reaction

        elif str(reaction.emoji) == choices.role_emojis["Healer"] and not members["Healer"]:
            members["Healer"] = user
            member_reactions["Healer"] = reaction

        elif str(reaction.emoji) == choices.role_emojis["DPS"] and len(members["DPS"]) < 3:
            members["DPS"].append(user)
            member_reactions["DPS"].append(reaction)

        await update_embed()  # Update the embed with the new role assignments

        # If all roles are filled, add a "✅" reaction to indicate the group is ready
        if members["Tank"] and members["Healer"] and len(members["DPS"]) == 3:
            await group_message.add_reaction("✅")

    async def update_embed(embed, members):
        # Update the embed fields with the current members
        embed.set_field_at(0, name="🛡️", value=members["Tank"].mention if members["Tank"] else "None", inline=False)
        embed.set_field_at(1, name="💚", value=members["Healer"].mention if members["Healer"] else "None", inline=False)

        # Update the DPS field with the current DPS members
        dps_value = "\n".join([dps_user.mention for dps_user in members["DPS"]] + ["None"] * (3 - len(members["DPS"])))
        embed.set_field_at(2, name="⚔️", value=dps_value, inline=False)

        try:
            # Try to edit the original embed message with the updated information
            await group_message.edit(embed=embed)
        except discord.errors.HTTPException as e:
            if e.status == 401:
                # If editing fails due to an invalid webhook token, recreate the message
                new_group_message = await interaction.followup.send(embed=embed)
                await group_message.delete()  # Delete the old message
                return new_group_message
            else:
                raise e

    # Function to check if a reaction is valid and relevant to the current group message
    def check_reaction(reaction, user):
        return user != bot.user and reaction.message.id == group_message.id

    # Event handler for when a user removes a reaction from the group message
    @bot.event
    async def on_reaction_remove(reaction):
        if reaction.message.id != group_message.id or reaction.user == bot.user:
            return

        # Handle the removal of a reaction by clearing the user's role
        if str(reaction.emoji) == choices.role_emojis["Tank"] and members["Tank"] == user:
            members["Tank"] = None

        elif str(reaction.emoji) == choices.role_emojis["Healer"] and members["Healer"] == user:
            members["Healer"] = None

        elif str(reaction.emoji) == choices.role_emojis["DPS"]:
            if user in members["DPS"]:
                members["DPS"].remove(reaction.user)

        await update_embed()  # Update the embed with the role removed

    # Function to check if all roles are filled and the group is complete
    def check_completion(reaction, user):
        return (
            reaction.message.id == group_message.id
            and str(reaction.emoji) == "✅"
                and str(reaction.emoji) == "✅"
                and user in [members["Tank"], members["Healer"], *members["DPS"]]
            )


    while True:
        reaction, user = await bot.wait_for('reaction_add', check=check_completion)

        if reaction.emoji == "✅" and user in [members["Tank"], members["Healer"], *members["DPS"]]:
            await group_message.delete()  # Delete the group message when the group is complete
            await interaction.followup.send(
                f"The group for {full_dungeon_name} has completed the dungeon. The message has been removed.",
                ephemeral=True
            )
            break
        else:
            await group_message.remove_reaction("✅", user)

# Run the bot with the token loaded from the environment variables
bot.run(TOKEN)
