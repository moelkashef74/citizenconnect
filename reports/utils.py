# utils.py
from geopy.geocoders import Nominatim

from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def geocode_location(latitude, longitude):
    """
    Convert latitude and longitude to a physical address.
    """
    geolocator = Nominatim(user_agent="reports")
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location and location.address:
            return location.address
        else:
            raise ValueError("Geocoding failed to return an address.")
    except GeocoderTimedOut:
        raise GeocoderTimedOut("Geocoding timed out.")
    except GeocoderServiceError:
        raise GeocoderServiceError("Geocoding service error.")
    except ValueError as e:
        raise ValueError(str(e))

# print(geocode_location(30.588743,31.488764))