import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("OPENWEATHER_API_KEY")
FLASK_API_URL = os.getenv("FLASK_API_URL", "http://127.0.0.1:5000")  # Default to local Flask API

# Check if the API_KEY is provided
if not API_KEY:
    st.error("API key not found. Please set the 'OPENWEATHER_API_KEY' in the .env file.")
    st.stop()

st.title("Weather Dashboard")
st.write("Enter a city name to fetch weather data.")

city = st.text_input("City Name", "Ho Chi Minh")

if st.button("Get Weather Data"):
    if city.strip():  # Check if the city name is not empty or just spaces
        with st.spinner("Fetching weather data..."):
            try:
                # Send POST request to Flask API
                response = requests.post(
                    f"{FLASK_API_URL}/get_weather",
                    json={"city": city.strip()},
                    timeout=10  # Set a timeout for the request
                )
                if response.status_code == 200:
                    data = response.json().get("data")
                    if data:
                        st.write(f"### Weather in {data['city']}")
                        st.write(f"- **Temperature:** {data['temperature']}°C")
                        st.write(f"- **Humidity:** {data['humidity']}%")
                        st.write(f"- **Weather:** {data['weather']}")
                        st.write(f"- **Timestamp:** {data['timestamp']}")
                    else:
                        st.error("No weather data available for the specified city.")
                else:
                    st.error(f"Failed to fetch weather data. Status Code: {response.status_code}. Please try again later.")
            except requests.exceptions.Timeout:
                st.error("The request timed out. Please try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching weather data: {e}")
    else:
        st.warning("Please enter a valid city name.")
