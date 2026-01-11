# makes API calls from OpenWeatherMap to log current wind conditions to a CSV file every 2 minutes

import requests
import csv
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY") # sensitive information goes in .env
LAT = os.getenv('pLAT')
LON = os.getenv('pLONG')
CITY = "CHICAGOLAND"

OUTPUT_FILE = "ground_truth_wind.csv"

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=imperial"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200: #client request received/processed by server
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "wind_speed_mph": data["wind"]["speed"],
                "wind_deg": data["wind"]["deg"], #direction (0=North, 90=East)
                "gust_mph": data["wind"].get("gust", "NA"), # gusts (if available, generally only if it's really really windy)
                "humidity": data["main"]["humidity"],
                "temp_f": data["main"]["temp"]
            }
        else:
            print(f"Error: {data.get('message', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"Network Error: {e}")
        return None

def main():
    print(f"--- Starting Weather Logger for {CITY} ---")
    print(f"Saving to: {OUTPUT_FILE}")
    print("Press ^+C to stop logging.\n")

    # create csv with headers IF doesn't exist (realistically only call the first time, unless the file is deleted afterward)
    try:
        with open(OUTPUT_FILE, mode='x', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["timestamp", "wind_speed_mph", "wind_deg", "gust_mph", "humidity", "temp_f"])
            writer.writeheader()
    except FileExistsError:
        pass # file exists, append to it in the loop below

    # constant writing to csv from API calls
    while True:
        weather_data = get_weather()
        if weather_data:
            with open(OUTPUT_FILE, mode='a', newline='') as file:
                # uncomment out the line 'pass' and comment out the writer lines to test without writing to file
                #writer = csv.DictWriter(file, fieldnames=["timestamp", "wind_speed_mph", "wind_deg", "gust_mph", "humidity", "temp_f"])
                #writer.writerow(weather_data)
                pass
            print(f"[{weather_data['timestamp']}] Wind: {weather_data['wind_speed_mph']} mph | Gust: {weather_data['gust_mph']} mph | Dir: {weather_data['wind_deg']}° | Humidity: {weather_data['humidity']}% | Temp: {weather_data['temp_f']}°")
        # OpenWeatherMap updates an individual location's current weather data about every 10 minutes, so there's no point bombarding the csv with identical data
        time.sleep(120)

if __name__ == "__main__":
    main()