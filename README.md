
**Commit message:**  
- Write README with setup & usage for CLI and Streamlit  
Commit.

---

## How to run locally
On bash type the following:
1) git clone https://github.com/hadil-ghazal/Weather-App.git
2) cd weather-app
3) python3 -m venv .venv && source .venv/bin/activate
4) pip install -r requirements.txt

# CLI with key
export OPENWEATHER_API_KEY="INSERT_KEY"
python weather_cli.py --city "Los Angeles, CA"

# CLI without key
python weather_cli.py --city "Los Angeles, CA"

# Streamlit 
export OPENWEATHER_API_KEY="INSERT_KEY"
streamlit run app.py
