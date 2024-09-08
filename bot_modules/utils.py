import asyncio
import re
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from bot_modules import constants

async def countdown(duration):
    print(f"Debug: Starting countdown for {duration} seconds.")
    
    while duration > 0:
    #    print(f"{duration} seconds remaining", end="\r")
        await asyncio.sleep(1)  # Wait for 1 second
        duration -= 1  # Decrement the duration
    
    # print("0 seconds remaining  ")  # Print final message
    print("Debug: Completed countdown.")

def format_dungeon_datetime(dungeon_datetime_str):
    # Define the format of the input string
    datetime_format = "%m/%d/%y %H:%M"
    print(f"Debug: Received input datetime string: {dungeon_datetime_str}")

    try:
        # Parse the input datetime string into a datetime object
        datetime_object = datetime.strptime(dungeon_datetime_str, datetime_format)
        print(f"Debug: Parsed datetime object: {datetime_object}")

        # Convert to Eastern Time (US/Eastern)
        est_time = datetime_object.astimezone(ZoneInfo("America/New_York"))
        print(f"Debug: Converted Eastern Time: {est_time}")

        # Convert Eastern Time to Unix timestamp
        unix_timestamp = int(est_time.timestamp())
        print(f"Debug: Unix timestamp: {unix_timestamp}")

        # Format the timestamp for Discord
        # Use 'f' for long date/time format (e.g., September 5, 2024 12:00 PM)
        formatted_timestamp = f"<t:{unix_timestamp}:F>"
        print(f"Debug: Formatted timestamp: {formatted_timestamp}")

    except (ValueError, TypeError) as e:
        # Handle errors and provide a default value
        print(f"Debug: Error parsing datetime: {e}")
        # Return a default formatted string if there's an error
        formatted_timestamp = "<t:0:F>"

    return formatted_timestamp

def get_unix_timestamp(dungeon_datetime_str):
    # Define the format of the input string
    datetime_format = "%m/%d/%y %H:%M"
    print(f"Debug: Received input datetime string: {dungeon_datetime_str}")

    try:
        # Parse the input datetime string into a datetime object
        datetime_object = datetime.strptime(dungeon_datetime_str, datetime_format)
        print(f"Debug: Parsed datetime object: {datetime_object}")

        # Convert to Eastern Time (US/Eastern)
        est_time = datetime_object.astimezone(ZoneInfo("America/New_York"))
        print(f"Debug: Converted Eastern Time: {est_time}")

        # Convert Eastern Time to Unix timestamp
        unix_timestamp = int(est_time.timestamp())
        print(f"Debug: Unix timestamp: {unix_timestamp}")

    except (ValueError, TypeError) as e:
        # Handle errors and provide a default value
        print(f"Debug: Error parsing datetime: {e}")
        # Return a default Unix timestamp for error cases (could be the Unix epoch start)
        unix_timestamp = 0

    return unix_timestamp

def calculate_time_difference(starting_timestamp):
    # Get the current Unix timestamp
    current_timestamp = int(time.time())
    print(f"Debug: Current Unix timestamp: {current_timestamp}")
    
    # Add one hour (3600 seconds) to the starting timestamp
    one_hour_later_timestamp = starting_timestamp + 3600
    print(f"Debug: Timestamp after adding one hour: {one_hour_later_timestamp}")

    # Calculate the difference in seconds between now and the future timestamp
    difference_in_seconds = one_hour_later_timestamp - current_timestamp
    print(f"Debug: Difference in seconds: {difference_in_seconds}")

    return difference_in_seconds

def mention_helper(server_id: str, role: str = None, difficulty: str = None):
    print(f"Comparing server_id: {server_id} with constants: "
          f"SG_DEV_SERVER_ID={constants.SG_DEV_SERVER_ID} and "
          f"SG_PROD_SERVER_ID={constants.SG_PROD_SERVER_ID}")

    # Determine the mention choices based on the server ID
    if str(server_id) in str(constants.SG_DEV_SERVER_ID):
        mention_choices = constants.DEV_MENTION_CHOICES
    elif str(server_id) in str(constants.SG_PROD_SERVER_ID):
        mention_choices = constants.PROD_MENTION_CHOICES
    else:
        return None

    # Initialize lists for role and difficulty mentions
    role_mentions = []
    difficulty_mentions = []

    # Define valid roles
    valid_roles = {"tank", "healer", "dps"}

    if role:
        if role.lower() in valid_roles:
            role_key = f"{role}_role"
            role_mention = mention_choices.get(role_key.lower())
            
            if role_mention:
                # Initialize difficulty_key for filtering role mentions
                difficulty_key = f"{difficulty}_role" if difficulty else None

                # Add all valid role mentions except the provided role, and exclude any difficulties
                role_mentions = [
                    mention for key, mention in mention_choices.items()
                    if key.lower() != role_key.lower() and any(valid_role in key.lower() for valid_role in valid_roles)
                ]
            else:
                print(f"No role mention found for key: {role_key}")
        else:
            print(f"Invalid role provided: {role}")

    if difficulty:
        difficulty_key = f"{difficulty}_role"
        difficulty_mention = mention_choices.get(difficulty_key.lower())
        
        if difficulty_mention:
            difficulty_mentions = [difficulty_mention]
        else:
            print(f"No difficulty mention found for key: {difficulty_key}")

    # Combine the lists: role mentions (excluding the provided role) and difficulty mentions
    mentions_to_return = role_mentions + difficulty_mentions

    # Print the mentions for debugging purposes
    print(f"Filtered role mentions (excluding the provided role and difficulties): {role_mentions}")
    print(f"Difficulty mentions: {difficulty_mentions}")
    print(f"Combined mentions: {mentions_to_return}")

    # Return the combined mentions
    return mentions_to_return


def extract_role_from_mention(mention: str) -> str:

    # Regular expression to extract the part between colons
    match = re.search(r'<:\w+:(\d+)>', mention)
    
    if match:
        # Extract the content inside the mention
        content = mention.split(':')[1]
        
        # Check for keywords
        if 'healer' in content:
            return 'healer'
        elif 'dps' in content:
            return 'dps'
        elif 'tank' in content:
            return 'tank'
    
    # Return an empty string if no keyword is found
    return ''

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