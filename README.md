# Weather Application

A PyQt5-based weather application that provides real-time weather updates and a 12-hour forecast for cities worldwide using the OpenWeatherMap API.

## Features
- **User-Friendly GUI:** A custom-designed interface using PyQt5.
- **Country and City Selection:** Select a country and city from dynamic dropdowns.
- **Weather Information:**
  - Real-time temperature, wind speed, humidity, and pressure.
  - Sunrise and sunset times (adjusted for the Tehran timezone).
- **12-Hour Forecast:** Displays weather predictions and icons for the next 12 hours.
- **Custom Window Controls:** Frameless and draggable window.

## Prerequisites
- Python 3.x
- PyQt5
- `requests` library
- `pycountry`
- `pytz`
- OpenWeatherMap API key

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AmirRghp/Weather-App.git
   cd Weather-App
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Replace the API key in Search function:
   ```bash
     API_KEY = "your_api_key_here"
4. Ensure the city.list.json file is in the project directory:
   - This file contains data for countries and cities used to populate the dropdowns.

## Usage
1. Run the application:
   ```bash
   python main.py
2. Select a country and city from the dropdown menus.
3. Click the Search button to fetch the weather data.
4. View the results and 12-hour forecast displayed in the GUI.

## Screenshot

## Video
