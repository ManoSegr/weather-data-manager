import requests
import sqlite3
from datetime import datetime
import json

class WeatherScraper:
    def __init__(self, db_name="weather_data.db"):
        self.db_name = db_name
        self.setup_database()
    
    def setup_database(self):
        """Create database and table if they don't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                temperature REAL,
                description TEXT,
                humidity INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database setup complete!")
    
    def get_weather_data(self, city):
        """Fetch weather data from OpenWeatherMap API"""
        # Free API key needed from openweathermap.org
        api_key = "bdb5ea698f2e9203483e9bb52ddbba02"  # Replace with actual API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                weather_info = {
                    'city': city,
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity']
                }
                return weather_info
            else:
                print(f"Error fetching data for {city}: {data.get('message', 'Unknown error')}")
                return None
                
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None
    
    def save_to_database(self, weather_data):
        """Save weather data to SQLite database"""
        if not weather_data:
            return False
            
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO weather_data (city, temperature, description, humidity)
            VALUES (?, ?, ?, ?)
        ''', (
            weather_data['city'],
            weather_data['temperature'],
            weather_data['description'],
            weather_data['humidity']
        ))
        
        conn.commit()
        conn.close()
        print(f"Weather data for {weather_data['city']} saved successfully!")
        return True
    
    def get_city_history(self, city, limit=10):
        """Retrieve historical weather data for a city"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT city, temperature, description, humidity, timestamp
            FROM weather_data
            WHERE city = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (city, limit))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_temperature_stats(self, city):
        """Get temperature statistics for a city"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                AVG(temperature) as avg_temp,
                MIN(temperature) as min_temp,
                MAX(temperature) as max_temp,
                COUNT(*) as total_records
            FROM weather_data
            WHERE city = ?
        ''', (city,))
        
        result = cursor.fetchone()
        conn.close()
        return result

def main():
    scraper = WeatherScraper()
    
    # List of cities to track
    cities = ["London", "Paris", "Tokyo", "New York", "Athens"]
    
    print("Starting weather data collection...")
    
    for city in cities:
        print(f"\nFetching weather for {city}...")
        weather_data = scraper.get_weather_data(city)
        
        if weather_data:
            scraper.save_to_database(weather_data)
            print(f"Temperature: {weather_data['temperature']}°C")
            print(f"Description: {weather_data['description']}")
            print(f"Humidity: {weather_data['humidity']}%")
        else:
            print(f"Failed to get data for {city}")
    
    # Display some statistics
    print("\n" + "="*50)
    print("WEATHER STATISTICS")
    print("="*50)
    
    for city in cities:
        history = scraper.get_city_history(city, 5)
        if history:
            print(f"\nLast 5 records for {city}:")
            for record in history:
                print(f"  {record[4]}: {record[1]}°C - {record[2]}")
            
            stats = scraper.get_temperature_stats(city)
            if stats and stats[3] > 0:  # If we have records
                print(f"  Stats: Avg: {stats[0]:.1f}°C, Min: {stats[1]}°C, Max: {stats[2]}°C")

if __name__ == "__main__":
    main()