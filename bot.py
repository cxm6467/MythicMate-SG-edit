import asyncio
import re
import discord
from discord.ext import commands
from discord import WebhookMessage, app_commands
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

members = {"Tank": None, "Healer": None, "DPS": []}
group_message: WebhookMessage
thread: WebhookMessage
lock = asyncio.Lock()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # Ensure command syncing with Discord
    try:
        await bot.tree.sync()  # Synchronize the command tree with Discord
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.event
async def on_reaction_add(reaction, user):
    # Print debug information about the reaction and user
    global group_message
    group_message = reaction.message
    print(f"Debug: Reaction added - Emoji: {reaction.emoji}, User: {user.name} ({user.id})")
    print(f"Debug: Group Message: {group_message.id} vs Reaction: {reaction.message.id}")

    if user == bot.user:
        print("Debug: Reaction is from the bot itself.")
        return

    async with lock:
        # Handle the "Clear Role" reaction
        if str(reaction.emoji) == choices.role_emojis.get("Clear Role"):
            print(f"Debug: Clear Role reaction detected by {user.name} ({user.id})")
            await reaction.message.thread.send(f"{user.mention} has left the group.")

            # Clear the user's role
            if user == members.get("Tank"):
                members["Tank"] = None
                print(f"Debug: Tank role cleared for {user.name} ({user.id})")
            elif user == members.get("Healer"):
                members["Healer"] = None
                print(f"Debug: Healer role cleared for {user.name} ({user.id})")
            elif user in members.get("DPS", []):
                members["DPS"].remove(user)
                print(f"Debug: DPS role cleared for {user.name} ({user.id})")

            # Remove the user's other role-related reactions
            for role, emoji in choices.role_emojis.items():
                if emoji != choices.role_emojis.get("Clear Role"):
                    if reaction.message is not None:
                        await reaction.message.remove_reaction(emoji, user)
                        print(f"Debug: Removed reaction {emoji} from message by {user.name} ({user.id})")

            # Update the embed
            print(f"Debug: Calling update_embed in clear_role check From on_reaction_add With: {reaction}")
            await update_embed(reaction)
            if reaction.message is not None:
                await reaction.message.remove_reaction(reaction.emoji, user)
                print("Debug: Embed updated and Clear Role reaction removed.")
            return

        # Prevent users from selecting multiple roles
        if user in [members["Tank"], members["Healer"], *members["DPS"]]:
            await reaction.message.remove_reaction(reaction.emoji, user)
            await user.send("You can only select one role.")
            print(f"Debug: User {user.name} ({user.id}) tried to select multiple roles. Reaction removed.")
            return

        # Assign the user to the selected role
        emoji_to_role = {
            choices.role_emojis["Tank"]: "Tank",
            choices.role_emojis["Healer"]: "Healer",
            choices.role_emojis["DPS"]: "DPS"
        }

        role = emoji_to_role.get(str(reaction.emoji))
        if role:
            if role == "Tank" and not members["Tank"]:
                members["Tank"] = user
                print(f"Debug: User {user.name} ({user.id}) assigned to Tank role.")
                await reaction.message.thread.send(f"{user.mention} has joined the group as Tank.")
            elif role == "Healer" and not members["Healer"]:
                members["Healer"] = user
                print(f"Debug: User {user.name} ({user.id}) assigned to Healer role.")
                await reaction.message.thread.send(f"{user.mention} has joined the group as Healer.")
            elif role == "DPS" and len(members["DPS"]) < 3:
                members["DPS"].append(user)
                print(f"Debug: User {user.name} ({user.id}) assigned to DPS role.")
                await reaction.message.thread.send(f"{user.mention} has joined the group as DPS.")

            # Update the embed
            print(f"Debug: Calling update_embed From on_reaction_add With: {reaction}")
            await update_embed(reaction)
            print("Debug: Embed updated with new role assignments.")

        # If all roles are filled, add a "✅" reaction
        if members["Tank"] and members["Healer"] and len(members["DPS"]) == 3:
            await reaction.message.add_reaction("✅")
            print("Debug: All roles filled, added ✅ reaction to indicate group is ready.")



async def update_embed(reaction):
    global group_message
    print("Debug: Updating embed:")
    
    #async with lock:
        # Print debug information about the embed update
    print("Debug: Updating embed with current members.")
    
    # Check if the message contains embeds
    if reaction.message.embeds:
        # Get the first embed from the message
        embed = group_message.embeds[0]
        
        # Create a mutable copy of the embed
        embed = discord.Embed.from_dict(embed.to_dict())
        
        # Update the embed fields with the current members
        embed.set_field_at(0, name="Tank", value=members["Tank"].mention if members["Tank"] else "None", inline=False)
        embed.set_field_at(1, name="Healer", value=members["Healer"].mention if members["Healer"] else "None", inline=False)

        # Update the DPS field with the current DPS members
        dps_value = "\n".join([dps_user.mention for dps_user in members["DPS"]] + ["None"] * (3 - len(members["DPS"])))
        embed.set_field_at(2, name="DPS", value=dps_value, inline=False)

        try:
            # Print debug information before attempting to edit the embed
            print("Debug: Attempting to edit the embed message.")
            
            # Try to edit the original embed message with the updated information
            await group_message.edit(embed=embed)

            # Print debug information after successful edit
            print("Debug: Embed message successfully edited.")
        except discord.errors.HTTPException as e:
            print(f"Debug: Exception occurred while editing embed: {e}")

            if e.status == 401:
                print("Debug: Invalid webhook token, recreating the message.")

                # If editing fails due to an invalid webhook token, recreate the message
                new_group_message = await group_message.channel.send(embed=embed)
                await group_message.delete()  # Delete the old message
                group_message = new_group_message

                # Print debug information after recreating the message
                print("Debug: New embed message created and old message deleted.")
            else:
                raise e
        else:
            print("Debug: No embed found in the message.")



@bot.event
async def on_reaction_remove(reaction, user):
    global group_message
    group_message = reaction.message
    print(f"{reaction}")
    if user == bot.user:
        return
        # Print debug information about the reaction removal

    await reaction.message.thread.send(f"A {reaction.emoji} has left the group")
    # Handle the removal of a reaction by clearing the user's role
    if str(reaction.emoji) == choices.role_emojis["Tank"] and members["Tank"] == user:
        members["Tank"] = None
    elif str(reaction.emoji) == choices.role_emojis["Healer"] and members["Healer"] == user:
        members["Healer"] = None
    elif str(reaction.emoji) == choices.role_emojis["DPS"]:
        if user in members["DPS"]:
            members["DPS"].remove(user)

    print(f"Debug: Calling update_embed From on_reaction_remove With: {reaction}")
    await update_embed(reaction)  # Update the embed with the role removed
    print("Debug: Embed updated after reaction removal.")


# Slash command to invoke the modal
@bot.tree.command(name="lfm", description="Start looking for members for a dungeon run.")
@app_commands.describe(difficulty="Choose a dungeon difficulty", dungeon='Choose a dungeon', level='Enter the key level or N/A', role="Enter your role")
@app_commands.choices(difficulty=choices.difficulty_choices)
@app_commands.choices(dungeon=choices.dungeon_choices)
@app_commands.choices(role=choices.role_choices)
async def lfm(interaction: discord.Interaction, difficulty: str, dungeon: str, level: str, role: str):
    global members, group_message, embed

    full_dungeon_name = dungeons.translate_dungeon_name(dungeon)

    if not full_dungeon_name:
        await interaction.response.send_message(f"Sorry, I couldn't recognize the dungeon name '{dungeon}'. Please try again with a valid name or abbreviation.", ephemeral=True)
        return

    # Initialize members based on role
    if "tank" in role.lower():
        members = {"Tank": interaction.user, "Healer": None, "DPS": []}
    elif "healer" in role.lower():
        members = {"Tank": None, "Healer": interaction.user, "DPS": []}
    elif "dps" in role.lower():
        members = {"Tank": None, "Healer": None, "DPS": [interaction.user]}
    else:
        members = {"Tank": None, "Healer": None, "DPS": []}

    lfmModal = modal.LFMModal(interaction, difficulty, full_dungeon_name, level, role, members, embed=discord.Embed(description=""), group_message=interaction.message)
    await interaction.response.send_modal(lfmModal)


    # Function to check if all roles are filled and the group is complete
    def check_completion(reaction, user):
        return (
            str(reaction.emoji) == "✅"
            and user in [members["Tank"], members["Healer"], *members["DPS"]]
        )

    while True:
        reaction, user = await bot.wait_for('reaction_add', check=check_completion)

        if reaction.emoji == "✅" and user in [members["Tank"], members["Healer"], *members["DPS"]]:
            async with lock:
                await reaction.message.delete()  # Delete the group message when the group is complete
            await interaction.followup.send(
                f"The group for {full_dungeon_name} has completed the dungeon. The message has been removed.",
                ephemeral=True
            )
            break
        else:
            async with lock:
                await reaction.message.remove_reaction("✅", user)
# Run the bot with the token loaded from the environment variables
bot.run(TOKEN)