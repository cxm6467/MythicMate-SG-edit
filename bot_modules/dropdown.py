import discord

class Dropdown(discord.ui.Select):
    def __init__(self, options=None, placeholder="Select an option"):
        # Call the parent class constructor with correct parameters
        super().__init__(placeholder=placeholder, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Handle the selected option here
        selected_value = self.values[0]  # Get the selected value
        await interaction.response.send_message(f"You selected: {selected_value}")

