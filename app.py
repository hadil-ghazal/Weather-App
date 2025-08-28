# app.py
import os
import re
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# ---------- setup ----------
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(page_title="Weather Viewer", page_icon="⛅", layout="centered")
st.title("⛅ Simple Weather App")
st.write("Enter a city, then click **Get Weather**.")

# ---------- user input ----------
city = st.text_input("City name", placeholder="e.g., Durham, London, Cairo")
get_weather = st.button("Get Weather")

# ---------- helpers ----------
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_openweather(city_name: str):
    """Return (data_dict, err_str) from OpenWeather."""
    params = {"q": city_name, "appid": API_KEY, "units": "metric"}
    try:
        r = requests.get(OPENWEATHER_URL, params=params, timeout=10)
        if r.status_code != 200:
            return None, f"API error ({r.status_code}): {r.text}"
        return r.json(), None
    except requests.RequestException as e:
        return None, f"Network error: {e}"

def fetch_wttr(city_name: str):
    """Keyless fallback using wttr.in. Returns normalized dict like OpenWeather."""
    try:
        r = requests.get(f"https://wttr.in/{city_name}?format=j1", timeout=10)
        r.raise_for_status()
        j = r.json()
        cur = j["current_condition"][0]
        return {
            "name": city_name.title(),
            "sys": {"country": ""},
            "main": {
                "temp": float(cur["temp_C"]),
                "feels_like": float(cur.get("FeelsLikeC", cur["temp_C"])),
                "humidity": int(cur["humidity"]),
            },
            "wind": {"speed": float(cur.get("windspeedKmph", 0)) / 3.6},  # km/h -> m/s
            "weather": [{"description": cur["weatherDesc"][0]["value"]}],
        }, None
    except Exception as e:
        return None, f"Fallback error: {e}"

# ---------- main ----------
if get_weather:
    if not city.strip():
        st.warning("Please enter a city.")
    else:
        data = None
        err = None
        source = None

        with st.spinner("Fetching weather..."):
            if API_KEY:  # try OpenWeather first
                data, err = fetch_openweather(city.strip())
                source = "OpenWeather"
                if err or not data:  # fall back
                    data, err = fetch_wttr(city.strip())
                    source = "wttr.in (fallback)"
            else:  # no key -> fallback
                data, err = fetch_wttr(city.strip())
                source = "wttr.in (fallback)"

        if err or not data:
            st.error(err or "No data returned.")
        else:
            name = data.get("name", city.title())
            sys = data.get("sys", {})
            country = sys.get("country", "")
            main = data.get("main", {})
            wind = data.get("wind", {})
            weather_list = data.get("weather", [])
            description_raw = weather_list[0]["description"] if weather_list else "N/A"

            # clean description a bit
            description_clean = re.sub(r"[^a-zA-Z\s]", "", description_raw).strip().title()

            temp = main.get("temp")
            feels = main.get("feels_like")
            humidity = main.get("humidity")
            wind_speed = wind.get("speed")

            # emoji hint
            emoji = "☀️"
            desc_low = description_clean.lower()
            if "cloud" in desc_low: emoji = "☁️"
            if "rain" in desc_low or "drizzle" in desc_low: emoji = "🌧️"
            if "storm" in desc_low or "thunder" in desc_low: emoji = "⛈️"
            if "snow" in desc_low: emoji = "❄️"
            if "mist" in desc_low or "fog" in desc_low or "haze" in desc_low: emoji = "🌫️"

            st.subheader(f"Weather in {name}, {country} {emoji}")
            st.write(f"**Condition:** {description_clean}")

            df = pd.DataFrame(
                {
                    "Metric": ["Temperature (°C)", "Feels Like (°C)", "Humidity (%)", "Wind (m/s)"],
                    "Value": [temp, feels, humidity, wind_speed],
                }
            )
            st.dataframe(df, use_container_width=True)
            st.bar_chart(df.set_index("Metric"))

            st.caption(f"Data source: {source} • Units: metric")
