Weather Data Manager
A professional Python application for collecting, storing, and analyzing weather data with SQLite database integration.
Features

Data Collection: Fetches real-time weather data from OpenWeatherMap API
Database Storage: Stores data in SQLite database with proper schema
Statistical Analysis: Calculates averages, trends, and historical comparisons
Report Generation: Creates comprehensive weather reports
Data Export: Exports data to CSV format for further analysis

Technologies Used

Python 3.x
SQLite Database
OpenWeatherMap API
Statistical Analysis Libraries

How It Works

Setup Database: Creates SQLite tables for weather data storage
Fetch Data: Retrieves weather information for multiple cities
Store & Analyze: Saves data and performs statistical calculations
Generate Reports: Creates detailed analysis reports

Sample Output
WEATHER DATABASE SUMMARY
========================
City         Records  Avg Temp  Last Update
London       7        12.4°C    2025-06-22 17:30:15
Athens       7        22.1°C    2025-06-22 17:30:16
Tokyo        7        18.7°C    2025-06-22 17:30:17
Business Applications

Weather Monitoring: Track conditions for business operations
Data Analysis: Historical weather pattern analysis
Reporting: Automated weather reports for stakeholders
API Integration: Demonstrates real-world API usage

Installation & Usage
bash# Clone repository
git clone https://github.com/ManoSegr/weather-data-manager.git

# Install dependencies
pip install requests

# Run the application
python weather_scraper.py
Database Schema

weather_data table with temperature, humidity, wind speed
Automatic data validation and error handling
Timestamp tracking for all records


Built with Python for reliable weather data management and analysis.
