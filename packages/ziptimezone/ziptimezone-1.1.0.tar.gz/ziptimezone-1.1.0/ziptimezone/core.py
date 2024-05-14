# core.py
from functools import lru_cache
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
from .globals import get_loaded_zip_data
from .mappings import map_timezone_to_region


def get_lat_long_for_zip(zip_code, country="US"):
    """
    Retrieve the latitude and longitude for a given ZIP code.

    Parameters:
        zip_code (str): The ZIP code for which geographic coordinates are requested.
        country (str): Country code to refine the search, default is 'US'.

    Returns:
        tuple: A tuple containing latitude and longitude (float, float) if found, otherwise (None, None).

    Raises:
        ValueError: If the ZIP code is not recognized or data is missing.
    """
    zip_data = get_loaded_zip_data()
    location = zip_data.get(zip_code)

    if location and location["latitude"] and location["longitude"]:
        return float(location["latitude"]), float(location["longitude"])
    else:
        raise ValueError(
            f"No valid geographic coordinates found for ZIP code {zip_code}."
        )


@lru_cache(maxsize=100)
def get_timezone_by_zip(zip_code):
    """
    Retrieves the timezone based on the provided ZIP code using geographic coordinates.

    Parameters:
        zip_code (str): The ZIP code for which the timezone is requested.

    Returns:
        str: The timezone string (e.g., 'America/New_York') if found,
             returns 'Unknown' if the timezone cannot be determined.
    """
    try:
        latitude, longitude = get_lat_long_for_zip(zip_code)
        tf = TimezoneFinder(in_memory=True)
        timezone = tf.timezone_at(lat=float(latitude), lng=float(longitude))
        return map_timezone_to_region(timezone) if timezone else "Unknown"
    except ValueError as e:
        return str(e)


def calculate_time_difference(zip1, zip2):
    """
    Calculate the time difference between two given ZIP codes.

    Parameters:
        zip1 (str): The first ZIP code.
        zip2 (str): The second ZIP code.

    Returns:
        str: A string describing the time difference if both ZIP codes are valid and in the US, otherwise an error message.
    """
    try:
        # Retrieve timezones for both zip codes
        timezone1 = get_timezone_by_zip(zip1)
        timezone2 = get_timezone_by_zip(zip2)

        if timezone1 == "Unknown" or timezone2 == "Unknown":
            return "One or both zip codes are invalid or non-US."

        # Convert timezones to pytz timezone objects
        tz1 = pytz.timezone(timezone1)
        tz2 = pytz.timezone(timezone2)

        # Current time in each timezone
        now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        time1 = now_utc.astimezone(tz1)
        time2 = now_utc.astimezone(tz2)

        # Calculate time difference in hours
        time_diff = (time1 - time2).total_seconds() / 3600  # Convert seconds to hours
        return f"Time difference between {zip1} and {zip2} is {time_diff:.2f} hours."

    except Exception as e:
        return str(e)
