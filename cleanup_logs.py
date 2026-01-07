# cleans up raw flight logs by removing sensitive location data (raw files and folders are in the .gitignore)

import pandas as pd

raw_file = 'RawFlightLogs/Raw_Jan6.4-41.csv'
new_file = '_'.join(raw_file.split('_')[1:]) # removes 'Raw_' prefix

# Read the flight logs CSV
df = pd.read_csv(raw_file)

# Remove latitude and longitude columns
df = df.drop(columns=['latitude', 'longitude'], errors='ignore')

# Write to new CSV
df.to_csv(f'FlightLogs/{new_file}', index=False)

print("Flight logs cleaned and saved to flight_logs_cleaned.csv")