import requests
import json
import time
from math import radians, sin, cos, sqrt, atan2
import geocoder
from colorama import Fore, Style

def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two points on the Earth
    R = 6371  # Radius of the Earth in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def mph_to_kph(mph):
    # Conversion from miles per hour to kilometers per hour
    kph = mph * 1.60934
    return kph

def get_iss_location():
    api_url = "https://api.wheretheiss.at/v1/satellites/25544"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Access the X-Rate-Limit-Remaining header
        x_rate_limit_remaining = response.headers.get('X-Rate-Limit-Remaining')

        # You have requests remaining, proceed with processing the response
        iss_data = json.loads(response.text)
        return iss_data, x_rate_limit_remaining

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print("Retrying in 60 seconds...")
        time.sleep(60)
        return None, None

def get_my_location():
    try:
        location = geocoder.ip('me')
        if location and location.latlng:
            return location.latlng
        else:
            print("Failed to retrieve location information.")
            return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    try:
        previous_location = None

        while True:
            iss_location, x_rate_limit_remaining = get_iss_location()
            my_latitude, my_longitude = get_my_location()

            if iss_location and my_latitude is not None and my_longitude is not None:
                print("Current ISS location:")
                print(f"Latitude: {iss_location['latitude']}")
                print(f"Longitude: {iss_location['longitude']}")
                print(f"Velocity: {iss_location['velocity']} miles per hour")

                print("\nYour current location:")
                print(f"Latitude: {my_latitude}")
                print(f"Longitude: {my_longitude}")

                if previous_location:
                    distance_to_target = calculate_distance(
                        iss_location['latitude'], iss_location['longitude'],
                        my_latitude, my_longitude
                    )
                    print("\nDistance from your location to ISS: ", end="")

                    # Set color based on distance
                    if distance_to_target > 8000:
                        print(f"{Fore.RED}{distance_to_target:.2f} kilometers{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.GREEN}{distance_to_target:.2f} kilometers{Style.RESET_ALL}")

                    # Convert velocity to kilometers per hour
                    velocity_kph = mph_to_kph(iss_location['velocity'])
                    print(f"Speed: {Fore.GREEN}{velocity_kph:.2f} kilometers per hour{Style.RESET_ALL}")


                # Update previous location
                previous_location = iss_location
            else:
                print("Failed to fetch ISS location or retrieve your location.")

            # Print rate limit information with a horizontal line separator
            print('-' * 50)

            # Countdown for 5 seconds before the next request
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

