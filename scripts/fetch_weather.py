import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
VC_API_KEY = os.getenv("VC_API_KEY")

def fetch_weather(city: str, datetime_obj: datetime):
    dt_str = datetime_obj.strftime("%Y-%m-%dT%H:00:00")
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{dt_str}?key={VC_API_KEY}&unitGroup=metric&include=hours"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        hour = data.get("days", [])[0].get("hours", [])[0]
        return {
            "datetime": hour.get("datetime"),
            "temp": hour.get("temp"),
            "precip": hour.get("precip"),
            "conditions": hour.get("conditions"),
            "icon": hour.get("icon"),
            "wind_speed": hour.get("windspeed")
        }
    else:
        print("Request failed:", response.status_code, response.text)
        return None

# Test example
if __name__ == "__main__":
    dt = datetime(2025, 1, 1, 9, 0)
    result = fetch_weather("chicago", dt)
    print(result)
