import asyncio
import re
import time
import discord
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dateutil.parser import parse
from bot_modules import constants


async def countdown(duration):
    print(f"Debug: Starting countdown for {duration} seconds.")
    
    while duration > 0:
    #    print(f"{duration} seconds remaining", end="\r")
        await asyncio.sleep(1)  # Wait for 1 second
        duration -= 1  # Decrement the duration
    
    # print("0 seconds remaining  ")  # Print final message
    print("Debug: Completed countdown.")

async def format_dungeon_datetime(dungeon_datetime_str, time_zone='America/New_York', user=None):
    print(f"Debug: Received input datetime string: '{dungeon_datetime_str}', time zone: {time_zone}")

    tz_name = constants.TIME_ZONE_MAPPING.get(time_zone.upper(), time_zone)
    if not tz_name:
        raise ValueError("Invalid time zone code. Use 'EST', 'CST', 'MST', or 'PST'.")

    formatted_timestamp = "<t:0:F>"
    errors = []

    try:
        # Normalize and parse the input string
        normalized_datetime_str = dungeon_datetime_str.strip()
        print(f"Debug: Normalized input datetime string: '{normalized_datetime_str}'")

        try:
            datetime_object = parse(normalized_datetime_str)
            print(f"Debug: Parsed datetime object: {datetime_object}")
        except (ValueError, TypeError) as e:
            errors.append(f"Error parsing datetime: {e}")
            return formatted_timestamp

        try:
            tz_info = ZoneInfo(tz_name)
            localized_time = datetime_object.astimezone(tz_info)
            print(f"Debug: Localized Time: {localized_time}")

            unix_timestamp = int(localized_time.timestamp())
            print(f"Debug: Unix timestamp: {unix_timestamp}")

            formatted_timestamp = f"<t:{unix_timestamp}:F>"
            print(f"Debug: Formatted timestamp: {formatted_timestamp}")

        except (ValueError, TypeError) as e:
            errors.append(f"Error converting to timezone or timestamp: {e}")

    except ValueError as e:
        errors.append(f"Error with timezone conversion: {e}")

    if errors and user:
        try:
            error_message = " | ".join(errors)
            await user.send(f"Error formatting datetime: {error_message}. Please check the format and try again.")
        except discord.DiscordException as send_error:
            print(f"Debug: Error sending message to user: {send_error}")

    return formatted_timestamp

def get_unix_timestamp(dungeon_datetime_str, time_zone='America/New_York'):
    print(f"Debug: Received input datetime string: '{dungeon_datetime_str}', time zone: {time_zone}")

    tz_name = constants.TIME_ZONE_MAPPING.get(time_zone.upper(), time_zone)
    if not tz_name:
        raise ValueError("Invalid time zone code. Use 'EST', 'CST', 'MST', or 'PST' or provide a valid IANA time zone.")

    unix_timestamp = 0

    try:
        # Normalize and parse the input string
        normalized_datetime_str = dungeon_datetime_str.strip()
        print(f"Debug: Normalized input datetime string: '{normalized_datetime_str}'")

        try:
            datetime_object = parse(normalized_datetime_str)
            print(f"Debug: Parsed datetime object: {datetime_object}")
        except (ValueError, TypeError) as e:
            print(f"Debug: Error parsing datetime: {e}")
            return unix_timestamp

        try:
            tz_info = ZoneInfo(tz_name)
            localized_time = datetime_object.astimezone(tz_info)
            print(f"Debug: Localized Time: {localized_time}")

            unix_timestamp = int(localized_time.timestamp())
            print(f"Debug: Unix timestamp: {unix_timestamp}")

        except (ValueError, TypeError) as e:
            print(f"Debug: Error converting to timezone or timestamp: {e}")

    except ValueError as e:
        print(f"Debug: Error with timezone conversion: {e}")

    return unix_timestamp

def calculate_time_difference(starting_timestamp, tz_name='America/New_York'):
    # Convert short time zone code to IANA time zone name if necessary
    tz_name = constants.TIME_ZONE_MAPPING.get(tz_name.upper(), tz_name)

    # Get the current time and convert it to a datetime object in EST
    current_timestamp = int(time.time())
    current_datetime_est = datetime.fromtimestamp(current_timestamp, tz=ZoneInfo('America/New_York'))
    print(f"Debug: Current datetime in EST: {current_datetime_est}")

    try:
        # Convert the starting Unix timestamp to a datetime object in the given time zone
        starting_datetime = datetime.fromtimestamp(starting_timestamp, tz=ZoneInfo('UTC'))
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