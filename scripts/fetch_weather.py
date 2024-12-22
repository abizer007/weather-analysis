import requests
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import os

# Constants
API_KEY = "your_openweathermap_api_key"
CITY = "Mumbai,IN"
API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
DATA_FILE = "data/weather_data.csv"
ANALYSIS_DIR = "data/analysis"

# Fetch live weather data
def fetch_weather():
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    weather_info = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
    }
    return weather_info

# Save data to CSV
def save_weather_data(weather_info):
    is_new_file = not os.path.exists(DATA_FILE)
    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=weather_info.keys())
        if is_new_file:
            writer.writeheader()
        writer.writerow(weather_info)

# Analyze and document weather data
def analyze_weather():
    if not os.path.exists(DATA_FILE):
        print("No data available to analyze.")
        return

    # Read data
    dates, temps, humidities = [], [], []
    with open(DATA_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(row["date"])
            temps.append(float(row["temperature"]))
            humidities.append(float(row["humidity"]))

    # Create analysis directory if it doesn't exist
    os.makedirs(ANALYSIS_DIR, exist_ok=True)

    # Summary
    avg_temp = sum(temps) / len(temps)
    avg_humidity = sum(humidities) / len(humidities)
    summary = (
        f"Weather Analysis for {CITY}\n"
        f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
        f"Average Temperature: {avg_temp:.2f}°C\n"
        f"Average Humidity: {avg_humidity:.2f}%\n"
    )
    with open(f"{ANALYSIS_DIR}/summary.txt", mode="w") as file:
        file.write(summary)

    # Plot data
    plt.figure(figsize=(10, 6))
    plt.plot(dates, temps, label="Temperature (°C)", marker="o")
    plt.plot(dates, humidities, label="Humidity (%)", marker="o")
    plt.title(f"Weather Trends for {CITY}")
    plt.xlabel("Date")
    plt.ylabel("Values")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{ANALYSIS_DIR}/weather_plot.png")

# Main function
if __name__ == "__main__":
    weather_data = fetch_weather()
    save_weather_data(weather_data)
    analyze_weather()
