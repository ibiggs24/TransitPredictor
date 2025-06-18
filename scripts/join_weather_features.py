import sqlite3
import pandas as pd
from datetime import datetime
from fetch_weather import fetch_weather

# Load stop_times with labels
conn = sqlite3.connect("smart_transit.db")
df = pd.read_sql_query("SELECT * FROM labeled_stop_times", conn)
conn.close()

# Clean up arrival_time format
df = df[df["arrival_time"].str.match(r"^\d{2}:\d{2}:\d{2}$", na=False)]
df["hour"] = df["arrival_time"].str.slice(0, 2).astype(int)
df = df[df["hour"].between(0, 23)]

# Simulate all stop times as occurring on Jan 1, 2025
df["timestamp"] = df["hour"].apply(lambda h: datetime(2025, 1, 1, h))

# Fetch hourly weather once per hour
weather_by_hour = {}
for h in df["hour"].unique():
    dt = datetime(2025, 1, 1, h)
    weather = fetch_weather("chicago", dt)
    if weather:
        weather_by_hour[h] = weather

# Map weather features to each row by hour
df["temp"] = df["hour"].map(lambda h: weather_by_hour[h]["temp"])
df["precip"] = df["hour"].map(lambda h: weather_by_hour[h]["precip"])
df["wind_speed"] = df["hour"].map(lambda h: weather_by_hour[h]["wind_speed"])
df["conditions"] = df["hour"].map(lambda h: weather_by_hour[h]["conditions"])

# Save to new table
conn = sqlite3.connect("smart_transit.db")
df.to_sql("labeled_with_weather", conn, if_exists="replace", index=False)
conn.close()

print("Weather enrichment complete. Saved to labeled_with_weather.")
