# bot_modules/modal.py
from discord import ui
import discord
from datetime import datetime
import bot_modules.choices as choices    # Import predefined choices
from datetime import datetime
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

# Define the modal for the slash command
class LFMModal(ui.Modal):
    def __init__(self, interaction: discord.Interaction, difficulty: str, dungeon: str = '', key_level: str = '', role: str = '', res: str = '', lust: str = '', title="Looking for Members"):
        super().__init__(title=title)
        
        self.difficulty = difficulty
        self.dungeon = dungeon
        self.key_level = key_level
        self.role = role
        self.res = res
        self.lust = lust

        # Set up text inputs with defaults provided
        self.dungeon_date = ui.TextInput(
            label="Date",
            placeholder="Enter a Date (DD.MM.YY)",
            required=True
        )
        
        self.dungeon_time = ui.TextInput(
            label="Time",
            placeholder="Enter a Time HH:MM EST (EST for now)",
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
        # Defer the interaction to prevent timeout errors
        await interaction.response.defer()

        group_title = f"Group for {self.dungeon}{' +' + self.key_level if self.key_level != 'N/A' else ''}"

        # Handle dungeon_date and dungeon_time formatting
        try:
            formatted_date = datetime.strptime(self.dungeon_date.value, "%d.%m.%y").strftime("%d.%m.%y")
        except (ValueError, AttributeError):
            formatted_date = "today"  # Assign default value if exception is thrown
        
        # Handle dungeon_time formatting and conversion to EST
        try:
            input_time = self.dungeon_time.value
            current_date = datetime.now().date()

            # Parse the input time in 24-hour format
            time_object = datetime.strptime(input_time, "%H:%M")
            datetime_combined = datetime.combine(current_date, time_object.time())

            # Assume input time is in UTC
            utc_time = datetime_combined.replace(tzinfo=timezone.utc)

            # Convert to Eastern Time (US/Eastern) without using pytz
            est_time = utc_time.astimezone(ZoneInfo("America/New_York"))

            # Format the time in 12-hour AM/PM format in EST
            formatted_time = est_time.strftime("%I:%M %p %Z")
        except (ValueError, AttributeError):
            formatted_time = "soon"  # Assign default value if exception is thrown

        # Create an embed message to display the group information
        embed = discord.Embed(
            title=group_title,
            description=(
                f"**Difficulty** {self.difficulty}"
                f"{self.key_level if self.key_level != 'N/A' else ''}\n"
                f"**Battle Res?**\t**{'✅' if self.res else '❌'}**\n"
                f"**Lust?**\t**{'✅' if self.lust else '❌'}**\n"
                f"**Dungeon Date:** {formatted_date}\n"
                f"**Dungeon Time:** {formatted_time}\n"
                f"{'**Notes:** ' + self.dungeon_note.value if self.dungeon_note.value else ''}\n"

            ),
            color=discord.Color.blue()
        )

        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

        # Initialize members based on the role the user selected
        if self.role.lower() == "tank":
            members = {"Tank": interaction.user, "Healer": None, "DPS": []}
        elif self.role.lower() == "healer":
            members = {"Tank": None, "Healer": interaction.user, "DPS": []}
        elif self.role.lower() == "dps":
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
        for emoji in choices.role_emojis.values():
            await group_message.add_reaction(emoji)

        # Create a thread for this group message using the channel
        await interaction.channel.create_thread(
            name=group_title,
            message=group_message,  # Attach the thread to the group message
            auto_archive_duration=1440,  # Auto-archive after 24 hours of inactivity
            reason="Starting group thread for dungeon run",
            type=discord.ChannelType.private_thread
        )