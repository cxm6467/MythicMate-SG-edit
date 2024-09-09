import asyncio
import re
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import discord

from bot_modules import constants

async def countdown(duration):
    print(f"Debug: Starting countdown for {duration} seconds.")
    
    while duration > 0:
    #    print(f"{duration} seconds remaining", end="\r")
        await asyncio.sleep(1)  # Wait for 1 second
        duration -= 1  # Decrement the duration
    
    # print("0 seconds remaining  ")  # Print final message
    print("Debug: Completed countdown.")

from datetime import datetime
from zoneinfo import ZoneInfo
import discord

async def format_dungeon_datetime(dungeon_datetime_str, time_zone='America/New_York', meridiem=24, user=None):
    print(f"Debug: Received input datetime string: '{dungeon_datetime_str}', time zone: {time_zone}, meridiem: {meridiem}")

    # Map short time zone codes to IANA time zone names
    time_zone_mapping = {
        'EST': 'America/New_York',    # Eastern Standard Time
        'CST': 'America/Chicago',     # Central Standard Time
        'MST': 'America/Denver',      # Mountain Standard Time
        'PST': 'America/Los_Angeles',  # Pacific Standard Time
        'AKST': 'America/Anchorage'  # Alaskan Standard Time
    }
    
    # Convert short time zone code to IANA time zone name
    tz_name = time_zone_mapping.get(time_zone.upper())
    if not tz_name:
        raise ValueError("Invalid time zone code. Use 'EST', 'CST', 'MST', or 'PST'.")

    # Initialize formatted timestamp
    formatted_timestamp = "<t:0:F>"

    try:
        # Determine the datetime format based on the meridiem value
        if meridiem == 12:
            datetime_format = "%m/%d/%y %I:%M %p"  # 12-hour format with AM/PM
        elif meridiem == 24:
            datetime_format = "%m/%d/%y %H:%M"  # 24-hour format
        else:
            raise ValueError("Invalid value for meridiem. Use 12 for 12-hour format or 24 for 24-hour format.")
        
        # Normalize the input string: Strip extra spaces and normalize AM/PM case
        normalized_datetime_str = dungeon_datetime_str.strip().upper()
        print(f"Debug: Normalized input datetime string: '{normalized_datetime_str}'")

        # Parse the input datetime string into a datetime object
        datetime_object = datetime.strptime(normalized_datetime_str, datetime_format)
        print(f"Debug: Parsed datetime object: {datetime_object}")

        # Convert to the specified time zone
        tz_info = ZoneInfo(tz_name)
        localized_time = datetime_object.replace(tzinfo=tz_info)
        print(f"Debug: Localized Time: {localized_time}")

        # Convert localized time to Unix timestamp
        unix_timestamp = int(localized_time.timestamp())
        print(f"Debug: Unix timestamp: {unix_timestamp}")

        # Format the timestamp for Discord
        formatted_timestamp = f"<t:{unix_timestamp}:F>"
        print(f"Debug: Formatted timestamp: {formatted_timestamp}")

    except (ValueError, TypeError) as e:
        # Handle errors and provide a default value
        print(f"Debug: Error parsing datetime: {e}")
        # Optionally, you can include the error details in the default formatted timestamp
        formatted_timestamp = "<t:0:F>"

        # Send a message to the user if provided
        if user:
            try:
                await user.send(f"Error formatting datetime: {e}. Please check the format and try again.")
            except discord.DiscordException as send_error:
                print(f"Debug: Error sending message to user: {send_error}")

    return formatted_timestamp


def get_unix_timestamp(dungeon_datetime_str, time_zone='America/New_York', meridiem=24):
    print(f"Debug: Received input datetime string: '{dungeon_datetime_str}', time zone: {time_zone}, meridiem: {meridiem}")

    # Map short time zone codes to IANA time zone names
    time_zone_mapping = {
        'EST': 'America/New_York',    # Eastern Standard Time
        'CST': 'America/Chicago',     # Central Standard Time
        'MST': 'America/Denver',      # Mountain Standard Time
        'PST': 'America/Los_Angeles',  # Pacific Standard Time
        'AKST': 'America/Anchorage'  # Alaskan Standard Time
    }
    
    # Convert short time zone code to IANA time zone name if necessary
    tz_name = time_zone_mapping.get(time_zone.upper(), time_zone)
    
    if not tz_name:
        raise ValueError("Invalid time zone code. Use 'EST', 'CST', 'MST', or 'PST' or provide a valid IANA time zone.")

    # Determine the datetime format based on the meridiem value
    if meridiem == 12:
        datetime_format = "%m/%d/%y %I:%M %p"  # 12-hour format with AM/PM
    elif meridiem == 24:
        datetime_format = "%m/%d/%y %H:%M"  # 24-hour format
    else:
        raise ValueError("Invalid value for meridiem. Use 12 for 12-hour format or 24 for 24-hour format.")
    
    # Initialize Unix timestamp
    unix_timestamp = 0
    
    try:
        # Normalize the input string: Strip extra spaces and normalize AM/PM case
        normalized_datetime_str = dungeon_datetime_str.strip().upper()
        print(f"Debug: Normalized input datetime string: '{normalized_datetime_str}'")

        # Parse the input datetime string into a datetime object
        datetime_object = datetime.strptime(normalized_datetime_str, datetime_format)
        print(f"Debug: Parsed datetime object: {datetime_object}")

        # Convert to the specified time zone
        tz_info = ZoneInfo(tz_name)
        localized_time = datetime_object.replace(tzinfo=tz_info)
        print(f"Debug: Localized Time: {localized_time}")

        # Convert localized time to Unix timestamp
        unix_timestamp = int(localized_time.timestamp())
        print(f"Debug: Unix timestamp: {unix_timestamp}")

    except (ValueError, TypeError) as e:
        # Handle errors and provide a default value
        print(f"Debug: Error parsing datetime: {e}")

    return unix_timestamp

def calculate_time_difference(starting_timestamp, tz_name='America/New_York'):
    # Map short time zone codes to IANA time zone names
    time_zone_mapping = {
        'EST': 'America/New_York',    # Eastern Standard Time
        'CST': 'America/Chicago',     # Central Standard Time
        'MST': 'America/Denver',      # Mountain Standard Time
        'PST': 'America/Los_Angeles',  # Pacific Standard Time
        'AKST': 'America/Anchorage'  # Alaskan Standard Time
    }

    # Convert short time zone code to IANA time zone name if necessary
    tz_name = time_zone_mapping.get(tz_name.upper(), tz_name)

    # Get the current time and convert it to a datetime object in EST
    current_timestamp = int(time.time())
    current_datetime_est = datetime.fromtimestamp(current_timestamp, tz=ZoneInfo('EST')).astimezone(ZoneInfo('America/New_York'))
    print(f"Debug: Current datetime in EST: {current_datetime_est}")

    try:
        # Convert the starting Unix timestamp to a datetime object in the given time zone
        starting_datetime = datetime.fromtimestamp(starting_timestamp, tz=ZoneInfo('EST'))
        localized_datetime = starting_datetime.astimezone(ZoneInfo(tz_name))
        print(f"Debug: Starting datetime in {tz_name}: {localized_datetime}")

        # Convert the localized datetime to EST
        starting_datetime_est = localized_datetime.astimezone(ZoneInfo('America/New_York'))
        print(f"Debug: Starting datetime in EST: {starting_datetime_est}")

    except Exception as e:
        print(f"Debug: Error with time zone conversion or datetime parsing: {e}")
        return None

    # Add one hour to the starting datetime in EST
    one_hour_later_datetime = starting_datetime_est + timedelta(hours=1)
    print(f"Debug: Datetime one hour later in EST: {one_hour_later_datetime}")

    # Calculate the difference in seconds between the current time in EST and the future timestamp
    difference_in_seconds = int(one_hour_later_datetime.timestamp()) - int(current_datetime_est.timestamp())
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