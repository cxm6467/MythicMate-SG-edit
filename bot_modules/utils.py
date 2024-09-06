import asyncio
import time
from datetime import datetime
from zoneinfo import ZoneInfo

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
