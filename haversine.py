# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python Snippet: Haversine Formula Implementation ----
# Description: This code calculates the great-circle distance between two points
#              on the Earth's surface given their latitude and longitude using
#              the Haversine formula.
# Author: OpenAI ChatGPT, Dr. Kostas Alexandridis
# Date: June 2024
# License: MIT License
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Import Libraries ----
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import math



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Haversine Function ----
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def haversine(lat1, lon1, lat2, lon2, units: str = 'km') -> float:
    """haversine: Haversine formula implementation

    Args:
        lat1 (double): Latitude of the first point in decimal degrees
        lon1 (double): Longitude of the first point in decimal degrees
        lat2 (double): Latitude of the second point in decimal degrees
        lon2 (double): Longitude of the second point in decimal degrees

    Returns:
        double: The great-circle distance between the two points in kilometers
    """

    # Check each of the latitude and longitude values to make sure they are within valid ranges
    if not (-90 <= lat1 <= 90):
        raise ValueError("Latitude 1 must be between -90 and 90 degrees.")
    if not (-90 <= lat2 <= 90):
        raise ValueError("Latitude 2 must be between -90 and 90 degrees.")
    if not (-180 <= lon1 <= 180):
        raise ValueError("Longitude 1 must be between -180 and 180 degrees.")
    if not (-180 <= lon2 <= 180):
        raise ValueError("Longitude 2 must be between -180 and 180 degrees.")
    if units not in ['km', 'miles']:
        raise ValueError("Units must be either 'km' or 'miles'.")

    # Convert latitude and longitude from degrees to radians (in place)
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of Earth in kilometers (use 3956 for miles)
    r = 6371.0 # kilometers
    
    # Calculate the distance
    distance = r * c
    
    if units == 'miles':
        distance *= 0.621371 # convert to miles
    
    return distance


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Example Usage ----
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    # Example coordinates (latitude and longitude in decimal degrees between Copenhagen and Athens)
    place1 = "Copenhagen"
    lat1, lon1 = 55.6761, 12.5683 # Copenhagen
    place2 = "Athens"
    lat2, lon2 = 37.9838, 23.7275 # Athens   
    
    distance_km = haversine(lat1, lon1, lat2, lon2, units='km')
    distance_miles = haversine(lat1, lon1, lat2, lon2, units='miles')

    print(f"Distance between {place1} and {place2}: {distance_km:,.2f} km")
    print(f"Distance between {place1} and {place2}: {distance_miles:,.2f} miles")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# End of Script ----
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
