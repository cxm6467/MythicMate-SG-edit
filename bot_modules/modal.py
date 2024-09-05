from discord import Webhook, ui
import discord
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import asyncio
from bot_modules import dungeons
import bot_modules.choices as choices

# Define the modal for the slash command
class LFMModal(ui.Modal):
    def __init__(self, interaction: discord.Interaction, difficulty: str, dungeon: str = '', key_level: str = '', role: str = '', res: str = '', lust: str = '', members:dict = [], embed:discord.Embed = discord.Embed(), group_message: Webhook = None, title="Looking for Members"):
        super().__init__(title=title)
        print(f"Initialized LFMModal with interaction user: {interaction.user}")
        self.user = interaction.user
        self.difficulty = difficulty
        self.dungeon = dungeon
        self.key_level = key_level
        self.role = role
        self.res = res
        self.lust = lust
        self.members = members
        self.embed = embed
        self.group_message = group_message

        # Set up text inputs with defaults provided
        self.dungeon_date = ui.TextInput(
            label="Date",
            placeholder="Enter a Date (MM/DD/YY)",
            required=True
        )
        
        self.dungeon_time = ui.TextInput(
            label="Time",
            placeholder="Enter a Time HH:MM 24hr EST (EST for now)",
            required=True
        )

        self.dungeon_note = ui.TextInput(
            label="Notes",
            placeholder="Optional Notes",
            required=False
        )
                
        # Add inputs to the modal
        self.add_item(self.dungeon_date)
        self.add_item(self.dungeon_time)
        self.add_item(self.dungeon_note)

        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        global thread
        # Defer the interaction to prevent timeout errors
        await interaction.response.defer()

        group_title = f"Group for {self.dungeon}{' +' + self.key_level if self.key_level != 'N/A' else ''}"

        # Handle dungeon_date and dungeon_time formatting
        try:
            formatted_date = datetime.strptime(self.dungeon_date.value, "%m/%d/%y").strftime("%m/%d/%y")
        except (ValueError, AttributeError):
            formatted_date = "today"  # Assign default value if exception is thrown
        
        # Handle dungeon_time formatting and conversion to EST
        try:
            input_time = self.dungeon_time.value # Make this EST

            # Parse the input time in 24-hour format
            time_object = datetime.strptime(input_time, "%H:%M")
            # datetime_combined = datetime.combine(current_date, time_object.time())

            # Convert to Eastern Time (US/Eastern) without using pytz
            est_time = time_object.astimezone(ZoneInfo("America/New_York"))

            # Format the time in 12-hour AM/PM format in EST
            formatted_time = est_time.strftime("%I:%M %p")
        except (ValueError, AttributeError):
            formatted_time = "soon"  # Assign default value if exception is thrown

        self.embed.title = group_title
        self.embed.description = (
                f"**Difficulty** {self.difficulty} "
                f"{self.key_level if self.key_level != 'N/A' else ''}\n"
                f"**Battle Res?**\t**{'✅' if self.res else '❌'}**\n"
                f"**Lust?**\t**{'✅' if self.lust else '❌'}**\n"
                f"📅   {formatted_date}\n"
                f"🕒   {formatted_time}\n"
                f"{'**Notes:** ' + '```' + self.dungeon_note.value +'```' if self.dungeon_note.value else ''}\n"
            )
        # Check if the dungeon note contains the word "caboose" (case insensitive)
        if "caboose" in self.dungeon_note.value.lower():
            self.embed.color = discord.Color.blue()
        elif "delacour" in self.dungeon_note.value.lower():
            self.embed.color = discord.Color.og_blurple()
        elif "nastaskia" in self.dungeon_note.value.lower():
            self.embed.color = discord.Color.blurple()
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

        # Send the embed message as a follow-up to the deferred response
        self.group_message = await interaction.followup.send(embed=self.embed)

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

        # Calculate deletion time (one hour from now)
        # Use the current EST time for calculating deletion time (not the dungeon time)
        current_time_est = datetime.now().astimezone(ZoneInfo("America/New_York"))
        try:
            deletion_time = current_time_est + timedelta(hours=1)
            deletion_time_str = deletion_time.strftime("%I:%M %p")
            
            # Calculate the duration to wait (in seconds)
            wait_duration = (deletion_time - current_time_est).total_seconds()
        except Exception as e:
            deletion_time_str = 'soon'
            wait_duration = 3600  # Fallback to 1 hour if calculation fails

        # Send a message in the thread indicating when it will be deleted
        await thread.send(
            f"{group_title}\n"
            f"Number of members: {len(self.members)}\n"
            f"This thread will be deleted at {deletion_time_str} (EST), one hour after dungeon start."
        )

        # Wait for the calculated duration
        await asyncio.sleep(wait_duration)

        # Delete the embed message and the thread after 60 seconds
        try:
            await self.group_message.delete()  # Delete the embed message
            await thread.delete()  # Delete the thread
        except discord.NotFound:
            print("Message or thread not found, perhaps it was deleted earlier.")
        except discord.Forbidden:
            print("Bot doesn't have permissions to delete message or thread.")
        except Exception as e:
            print(f"An error occurred: {e}")
