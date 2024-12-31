from flask import Flask, jsonify, request
import requests
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os
from flask_cors import CORS
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all domains
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get API key and database password from environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Validate environment variables
if not API_KEY or not DB_PASSWORD:
    raise ValueError("Environment variables 'OPENWEATHER_API_KEY' and 'DB_PASSWORD' must be set.")

# Database connection function
def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=DB_PASSWORD,
            database="weather_data"
        )
    except mysql.connector.Error as e:
        logging.error(f"Database connection error: {e}")
        return None

def fetch_weather(city, api_key):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Log the raw response for debugging
        logging.info(f"Fetched data: {data}")
        
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["main"],  # Weather description (e.g., "Clear")
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return None

# Save weather data to MySQL database
def save_to_db(weather_data):
    db = connect_to_db()
    if not db:
        logging.error("Failed to connect to the database.")
        return

    try:
        cursor = db.cursor()
        query = """
            INSERT INTO weather (city, temperature, humidity, weather, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            weather_data["city"],
            weather_data["temperature"],
            weather_data["humidity"],
            weather_data["weather"],
            weather_data["timestamp"]
        ))
        db.commit()
        logging.info("Weather data saved to the database successfully.")
    except mysql.connector.Error as e:
        logging.error(f"Error saving to database: {e}")
    finally:
        cursor.close()
        db.close()

# Endpoint to get weather data and save to DB
@app.route('/get_weather', methods=['GET', 'POST'])
def get_weather():
    if request.method == 'POST':
        data = request.json
        city = data.get('city')
        if not city:
            return jsonify({"error": "City name is required"}), 400

        weather_data = fetch_weather(city, API_KEY)
        if weather_data:
            save_to_db(weather_data)  # Save data to DB
            return jsonify({"data": weather_data}), 200
        else:
            return jsonify({"error": "Failed to fetch weather data"}), 500

    elif request.method == 'GET':
        city = request.args.get('city')
        if not city:
            return jsonify({"error": "City name is required"}), 400

        weather_data = fetch_weather(city, API_KEY)
        if weather_data:
            save_to_db(weather_data)  # Save data to DB
            return jsonify({"data": weather_data}), 200
        else:
            return jsonify({"error": "Failed to fetch weather data"}), 500

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
