import os
import re
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# ---------- setup ----------
# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Basic page config
st.set_page_config(page_title="Weather Viewer", page_icon="⛅", layout="centered")

st.title("⛅ Simple Weather App")
st.write("Enter a city, then click **Get Weather**.")

# ---------- user input ----------
city = st.text_input("City name", placeholder="e.g., Durham, London, Cairo")
get_weather = st.button("Get Weather")

# ---------- helper: call OpenWeather ----------
def fetch_weather(city_name: str):
    """Return dict with weather data or None on error."""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"  # change to 'imperial' for °F
    }
    try:
        resp = requests.get(base_url, params=params, timeout=10)
        if resp.status_code != 200:
            return None, f"API error ({resp.status_code}): {resp.text}"
        return resp.json(), None
    except requests.RequestException as e:
        return None, f"Network error: {e}"

# ---------- main action ----------
if get_weather:
    # Guardrails
    if not API_KEY:
        st.error("Missing API key. Put it in a `.env` file as OPENWEATHER_API_KEY.")
    elif not city.strip():
        st.warning("Please enter a city.")
    else:
        with st.spinner("Fetching weather..."):
            data, err = fetch_weather(city.strip())

        if err:
            st.error(err)
        elif not data:
            st.error("No data returned.")
        else:
            # Pull useful bits
            name = data.get("name", city.title())
            sys = data.get("sys", {})
            country = sys.get("country", "")
            main = data.get("main", {})
            wind = data.get("wind", {})
            weather_list = data.get("weather", [])
            description_raw = weather_list[0]["description"] if weather_list else "N/A"

            # Tiny regex cleanup example (remove non-letters, title case)
            description_clean = re.sub(r"[^a-zA-Z\s]", "", description_raw).strip().title()

            temp = main.get("temp")
            feels = main.get("feels_like")
            humidity = main.get("humidity")
            wind_speed = wind.get("speed")

            # Emoji hint based on description
            emoji = "☀️"
            desc_low = description_clean.lower()
            if "cloud" in desc_low: emoji = "☁️"
            if "rain" in desc_low or "drizzle" in desc_low: emoji = "🌧️"
            if "storm" in desc_low or "thunder" in desc_low: emoji = "⛈️"
            if "snow" in desc_low: emoji = "❄️"
            if "mist" in desc_low or "fog" in desc_low or "haze" in desc_low: emoji = "🌫️"

            st.subheader(f"Weather in {name}, {country} {emoji}")
            st.write(f"**Condition:** {description_clean}")

            # Show metrics in a small table and chart
            df = pd.DataFrame(
                {
                    "Metric": ["Temperature (°C)", "Feels Like (°C)", "Humidity (%)", "Wind (m/s)"],
                    "Value": [temp, feels, humidity, wind_speed],
                }
            )
            st.dataframe(df, use_container_width=True)

            # Simple bar chart of the numeric metrics
            chart_df = df.set_index("Metric")
            st.bar_chart(chart_df)

            # Little footer
            st.caption("Data: OpenWeather • Units: metric • You can change to 'imperial' in the code if you prefer °F.")
