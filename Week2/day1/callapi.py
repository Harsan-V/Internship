import requests
import pandas as pd

# API endpoint
url = "https://opensky-network.org/api/states/all"

# Get data
response = requests.get(url)
data = response.json()

# Extract states list
states = data["states"]

# Column names from OpenSky API
columns = [
    "icao24","callsign","origin_country","time_position","last_contact",
    "longitude","latitude","baro_altitude","on_ground","velocity",
    "true_track","vertical_rate","sensors","geo_altitude",
    "squawk","spi","position_source"
]

# Convert to DataFrame
df = pd.DataFrame(states, columns=columns)

# Save to Excel
df.to_excel("opensky_flights.xlsx", index=False)

print("Data exported successfully!")