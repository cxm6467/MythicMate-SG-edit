from cProfile import label
from discord import Webhook, ui
import discord
from datetime import date, datetime
from bot_modules import dungeons, utils
import bot_modules.choices as choices

from discord import ui, Embed, Interaction
from datetime import datetime

# Ensure `choices` module is correctly imported
# import choices 

# Define the modal for the slash command
class LFMModal(ui.Modal):
    def __init__(self, interaction: discord.Interaction, difficulty: str, dungeon: str = '', level: str = '', role: str = '', members: list = [], embed: discord.Embed = discord.Embed(), group_message: discord.Webhook = None, title="Looking for Members"):
        super().__init__(title=title)
        
        # Debugging print statement
        print(f"Initialized LFMModal with interaction user: {interaction.user}")
        
        # Instance variables
        self.user = interaction.user
        self.difficulty = difficulty
        self.dungeon = dungeon
        self.level = level
        self.role = role
        self.members = members
        self.embed = embed
        self.group_message = group_message
        self.formatted_date_time = datetime.now()

        # Set up text inputs with defaults provided
        self.dungeon_date_time = ui.TextInput(
            label="Date",
            placeholder="Enter a Date and Time (MM/DD/YY HH:MM) EST 24hr [e.g., 09/05/24 20:00]",
            required=True
        )

        # Setup Select components with the provided options
        self.dungeon_tz = ui.TextInput(
            placeholder="Select a Timezone",
            label="Timezone"
        )
        self.dungeon_meridiem = ui.TextInput(
            placeholder="Select AM or PM",
            label="Meridiem"
        )

        self.dungeon_note = ui.TextInput(
            label="Notes",
            placeholder="Optional Notes",
            required=False
        )

        # Add inputs to the modal
        self.add_item(self.dungeon_date_time)
        self.add_item(self.dungeon_tz)
        self.add_item(self.dungeon_meridiem)
        self.add_item(self.dungeon_note)
                
        self.interaction = interaction


    async def on_submit(self, interaction: discord.Interaction):
        global thread
        # Defer the interaction to prevent timeout errors
        await interaction.response.defer()

        group_title = f"Group for {self.dungeon}{' +' + self.level if self.level != 'N/A' else ''}"

        # Convert datetime object to Unix timestamp
        timestamp = utils.format_dungeon_datetime(self.dungeon_date_time.value) if self.dungeon_date_time.value else datetime.now().strftime("%m/%d/%y %H:%M")

        self.embed.title = group_title
        self.embed.description = (
                f"**Difficulty** {self.difficulty} "
                f"{self.level if self.level != 'N/A' else ''}\n"
                f"📅\n   {timestamp}\n"
                f"{'**Notes:** ' + '```' + self.dungeon_note.value +'```' if self.dungeon_note.value else ''}\n"
            )
        
        # Check if the dungeon note contains the word "caboose" (case insensitive)
        if "caboose" in self.dungeon_note.value.lower():
            self.embed.color = discord.Color.blue()
        elif "delacour" or "nastaskia" in self.dungeon_note.value.lower():
            self.embed.color = discord.Color(0xFFFFFF)
        else:
            self.embed.color = discord.Color.red()


        kwargs = {'name': interaction.user.display_name}
        if interaction.user.avatar and interaction.user.avatar.url:
            kwargs['icon_url'] = interaction.user.avatar.url

        self.embed.set_author(**kwargs)

        # Set a thumbnail or image URL for the embed (use your own URL here)
        self.embed.set_thumbnail(url=dungeons.dungeon_urls[self.dungeon])

        # Populate the embed with initial values for Tank, Healer, and DPS roles
        self.embed.add_field(name="<:wow_tank:868737094242152488> Tank", value=self.members["Tank"].mention if self.members["Tank"] else "None", inline=False)
        self.embed.add_field(name="<:wow_healer:868737094258950144> Healer", value=self.members["Healer"].mention if self.members["Healer"] else "None", inline=False)

        # Add one field for DPS with placeholders for up to three DPS members
        dps_value = "\n".join([dps_user.mention for dps_user in self.members["DPS"]] + ["None"] * (3 - len(self.members["DPS"])))
        self.embed.add_field(name="<:wow_dps:868737094011486229> DPS", value=dps_value, inline=False)
        
        mention_list = utils.mention_helper(interaction.guild.id, utils.extract_role_from_mention(self.role), self.difficulty)
        print(f"Debug: mention_list for guild_id={interaction.guild.id}, role={self.role}, difficulty={self.difficulty} is {mention_list}")
        mention_list_str = ' '.join(mention_list)

        self.group_message = await interaction.followup.send(
            content=mention_list_str,  # Send the mention list as text content
            embed=self.embed  # Send the embed message
        )

        # Wait for the calculated duration
        wait_ts = utils.get_unix_timestamp(self.dungeon_date_time.value) + ( 60 * 60 )
        wait = utils.calculate_time_difference(wait_ts)

        # Add reaction emojis for Tank, Healer, DPS, and Clear Role
        for emoji in choices.role_emojis.values():
            await self.group_message.add_reaction(emoji)

        # Create a thread for this group message using the channel
        thread = await interaction.channel.create_thread(
            name=group_title,
            message=self.group_message,  # Attach the thread to the group message
            auto_archive_duration=60,  # Auto-archive after 60 minutes of inactivity
            reason="Starting group thread for dungeon run",
            type=discord.ChannelType.private_thread
        )

        await thread.send(
            f"Good luck on your dungeon run!\n"
            f"Listing will be deleted at <t:{wait_ts}:F>\n"
        )
        
        await utils.countdown(wait)

        async def delete_message_and_thread(self):
            print("Attempting to delete the message and thread.")
            
            # Add checks to verify that the objects are not None
            if not self.group_message:
                print("The group_message object is None.")
            if not thread:
                print("The thread object is None.")
            
            try:
                if self.group_message:
                    print(f"Deleting message: {self.group_message.id}")
                    await self.group_message.delete()  # Delete the embed message
                else:
                    print("No message to delete.")
                
                if thread:
                    print(f"Deleting thread: {thread.id}")
                    await thread.delete()  # Delete the thread
                else:
                    print("No thread to delete.")
                
            except discord.NotFound:
                print("Message or thread not found, perhaps it was deleted earlier.")
            except discord.Forbidden:
                print("Bot doesn't have permissions to delete message or thread.")
            except discord.HTTPException as e:
                print(f"HTTP error occurred: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        await delete_message_and_thread(self)
