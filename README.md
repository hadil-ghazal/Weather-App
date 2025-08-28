## How to run locally
On bash type the following:
1) git clone https://github.com/hadil-ghazal/Weather-App.git
2) cd weather-app
3) Create and activate a virtual environment by typing the folllowing into bash:
     1)  python3 -m venv .venv
     2)  source .venv/bin/activate
  - If no module is named venv error shows up, type the following in bash:
      1)    python3 -m pip install --upgrade pip
      2)    python3 -m pip install virtualenv
      3)    python3 -m virtualenv .env
      4)    source .venv/bin/activate
4) pip install -r requirements.txt
   
6) Streamlit App Launch 
    1) With no Key requirement:
            1) streamlit run app.py
          ##OR
    3) With an API Key:
            1) Sign up for a free API key at OpenWeather
            2) Create a file called .env at the project root
            3) Inside .env, paste your key within the following: OPENWEATHER_API_KEY=your_api_key
            4) Steamlit run app.py



