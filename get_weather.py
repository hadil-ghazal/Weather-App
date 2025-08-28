import os
import requests
from dotenv import load_dotenv

#Load .env 
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

#Buffer for protection
if not API_KEY:
    raise RuntimeError("No OPENWEATHER_API_KEY found. Check .env file")

def get_weather(city: str):
    """
    Getting weather for the city of interest and printing it neatly
    """
    #Build the API URL and query 
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric" # metric for celcius
    }
    #Making the request
    resp = requests.get(url, params=params, timeout=10)
    #Bad Response for 4xx or 5xx
    resp.raise_for_status()
    data = resp.json()
    # Print Fields
    name = data.get("name", city)
    main = data.get("weather", [{}])[0].get("main", "Unknown")
    desc = data.get("weather", [{}])[0].get("description", "Unknown").title()
    temp = data.get("main", {}).get("temp", "?")
    feels = data.get("main", {}).get("feels_like", "?")

    print(f"City: {name}")
    print(f"conditions: {main} - {desc}")
    print(f"Temerature: {temp} Celcius (feels like {feels} Celcius)")

if __name__ == "__main__":
    get_weather("Anaheim,US")