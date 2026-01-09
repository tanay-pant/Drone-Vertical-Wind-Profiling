# cleans up raw flight logs by removing sensitive location data (raw files and folders are in the .gitignore)

import pandas as pd
from pathlib import Path

def cleanup_flight_logs(raw_file):
    # Get the output filename by removing 'Raw_' prefix
    new_file = '_'.join(raw_file.split('_')[1:])
    
    # Read the flight logs CSV
    df = pd.read_csv(f'RawFlightLogs/{raw_file}')
    
    # Remove latitude and longitude columns (and unnecessary columns) and convert height from feet to meters
    df = df.drop(columns=['latitude', 'longitude'], errors='ignore')
    df['height_above_takeoff(meters)'] = (df['height_above_takeoff(feet)'] * 0.3048).round(2)
    df = df.drop(columns=['height_above_takeoff(feet)', 'height_above_ground_at_drone_location(feet)', 'ground_elevation_at_drone_location(feet)'], errors='ignore')
    
    # change datetime format from UTC to CST
    df['datetime(utc)'] = pd.to_datetime(df['datetime(utc)']).dt.tz_localize('UTC').dt.tz_convert('US/Central').dt.tz_localize(None)
    df = df.rename(columns={'datetime(utc)': 'timestamp'})
    
    # Write to new CSV
    df.to_csv(f'FlightLogs/{new_file}', index=False)
    print(f"Cleaned: {raw_file} -> {new_file}")

# Process all files in RawFlightLogs/
raw_logs_dir = Path('RawFlightLogs')
for raw_file in sorted(raw_logs_dir.glob('Raw_*.csv')):
    cleanup_flight_logs(raw_file.name)

print("All flight logs cleaned and saved!")