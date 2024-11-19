# International Space Station Tracker

## Overview
The **International Space Station (ISS) Tracker** is a Python application that provides real-time information about the location of the ISS and calculates the distance from your current location to the ISS. The application uses the Haversine formula to compute distances and integrates with an external API to fetch the ISS's current position and velocity.

## Features
- Retrieves the current latitude and longitude of the ISS.
- Fetches the user's current location using IP geolocation.
- Calculates the distance from the user's location to the ISS.
- Converts the ISS's velocity from miles per hour to kilometers per hour.
- Displays distance with color coding based on proximity to the ISS.
- Continuously updates the information every 5 seconds.

## Requirements
To run this application, ensure you have installed required packages:
 
 pip install -r requirements.txt


