from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic , QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests
import json
import pycountry
from datetime import datetime, timedelta
import pytz
import sys


class Weather(QMainWindow):
    def __init__(self):
        super(Weather, self).__init__()
        uic.loadUi('./ui/WeatherUi.ui', self)

        # remove windows title bar
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # set main background transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # button clicks on top bar
        # minimize window
        self.btnMinus.clicked.connect(self.showMinimized)
        # Close window
        self.btnClose.clicked.connect(self.close)
        #fill Combo Boxes
        self.fillCountryCmb()
        self.fillCityCmb()
        #self activate Country combo box when it changes and update city combo box
        self.cmbCountry.activated.connect(self.fillCityCmb)
        #button clicked event
        self.BtnSearch.clicked.connect(self.Search)

        #save the weater of city
        self.weather = ''

    def fillCountryCmb(self):
        try:
            # open city name json file and get country name by code and convert it to full name and put it in Combo
            file_path = "city.list.json"
            with open(file_path, "rt", encoding="utf-8") as f:
                cities = json.load(f)

            country_codes = {city["country"] for city in cities}

            country_full_names = {}
            for code in sorted(country_codes):
                country = pycountry.countries.get(alpha_2=code)
                if country:
                    country_full_names[country.name] = code
                else:
                    country_full_names[f"Unknown code"]= code

            for c in sorted(country_full_names):
                if c != "Unknown code":
                    self.cmbCountry.addItem(str(c),str(country_full_names[c]))

        except Exception as e:
            print(e)

    def fillCityCmb(self):
        try:
            # clear the city combo box
            self.cmbCity.clear()
            # get  current data of country combo box
            currantCountryCode = self.cmbCountry.currentData()
            file_path = "city.list.json"
            with open(file_path, "rt", encoding="utf-8") as f:
                cities = json.load(f)
            # Filter cities by the country code
            cities_in_country = [city["name"] for city in cities if city["country"] == currantCountryCode]
            # if there was a city  put it in combo box
            if cities_in_country:
                for c in sorted(cities_in_country):
                    self.cmbCity.addItem(str(c))
        except Exception as e:
            print(e)

    def Search(self):
        try:
            city = self.cmbCity.currentText()
            API_KEY = "7063176bf1f326933ff6182399353e3d"
            BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

            request_url = f"{BASE_URL}?appid={API_KEY}&q={city}"  # query of get weather with city name
            response = requests.get(request_url)

            if response.status_code == 200: # if the status code was 200
                data = response.json()  # put json response in data
                self.showWeather(data)
                self.showForeCast()

        except Exception as e:
            print(e)

    def showWeather(self, data):
        try:
            weather_desc = data["weather"][0]["description"]  # get the info of weather in json
            weather_id = int(data["weather"][0]["id"])
            self.txtweather_2.setText(weather_desc)
            self.txtweather.setText("")

            if weather_id >= 200 and weather_id <= 232: # Thunderstorms
                pixmap = QPixmap("images/09d.png")
                self.txtweather.setPixmap(pixmap)
            elif weather_id >= 300 and weather_id <= 321:  # Drizzle
                pixmap = QPixmap("images/10d.png")
                self.txtweather.setPixmap(pixmap)
            elif weather_id >= 500 and weather_id <= 504:  # Rain
                pixmap = QPixmap("images/10n.png")
                self.txtweather.setPixmap(pixmap)
            elif weather_id == 511: # freezing Rain
                pixmap = QPixmap("images/09n.png")
                self.txtweather.setPixmap(pixmap)
            elif weather_id >= 520 and weather_id <= 531: # Rain
                pixmap = QPixmap("images/10d.png")
                self.txtweather.setPixmap(pixmap)
            elif weather_id >= 600 and weather_id <= 622: # Snow
                pixmap = QPixmap("images/13d.png")
                self.txtweather.setPixmap(pixmap)
            elif weather_id >= 600 and weather_id <= 622: # Atmosphere
                pixmap = QPixmap("images/03d.png")
                self.txtweather.setPixmap(pixmap)
            elif weather_id == 800 : # Clear
                pixmap = QPixmap("images/01n.png")
                self.txtweather.setPixmap(pixmap)
            elif weather_id == 801 or weather_id == 802: # few clouds and  scattered clouds
                pixmap = QPixmap("images/02n.png")
                self.txtweather.setPixmap(pixmap)
            elif weather_id == 803 or weather_id == 804: # overcast clouds and  broken clouds
                pixmap = QPixmap("images/03d.png")
                self.txtweather.setPixmap(pixmap)

            #iran time zone
            iran_timezone = pytz.timezone("Asia/Tehran")
            #calculate Sunrise time
            sunrise_time = datetime.utcfromtimestamp(data["sys"]["sunrise"])
            sunrise_time = sunrise_time.replace(tzinfo=pytz.utc).astimezone(iran_timezone).strftime('%H:%M:%S')
            self.lblSunrise.setText(sunrise_time)
            # calculate Sunset time
            sunset_time = datetime.utcfromtimestamp(data["sys"]["sunset"])
            sunset_time = sunset_time.replace(tzinfo=pytz.utc).astimezone(iran_timezone).strftime('%H:%M:%S')
            self.lblSunSet.setText(sunset_time)
            # calculate Wind speed
            wind_Speed = data["wind"]["speed"]
            self.lblWindSpeed.setText(f"{str(wind_Speed)} m/s")
            #temp
            temp = round(data['main']['temp'] - 273.15, 2)  # get temp info and convert it from kelvin to celcius
            self.lblTemp.setText(f"{temp} C")
            #Pressure
            pressure = data["main"]["pressure"]
            self.lblPressure.setText(f"{str(pressure)} Pa")
            # humidity
            humidity = data["main"]["humidity"]
            self.lblhumidity.setText(f"{str(humidity)} %")



        except Exception as e:
            print(e)

    def showForeCast(self):
        try:
            city = self.cmbCity.currentText()
            API_KEY = "7063176bf1f326933ff6182399353e3d"
            BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

            request_url = f"{BASE_URL}?appid={API_KEY}&q={city}"  # query of get weather with city name
            response = requests.get(request_url)

            if response.status_code == 200:  # if the status code was 200
                data = response.json()  # put json response in data

            # Calculate times for 3, 6, 9, and 12 hours ahead
            hours_ahead_list = [3, 6, 9, 12]
            current_time = datetime.utcnow()
            forecast_hours = {hour: current_time + timedelta(hours=hour) for hour in hours_ahead_list}

            # Find the forecast entries closest to each target time (3, 6, 9, and 12 hours ahead)
            forecast_data = {}
            forcast_id = [] # get the id of the weather
            for entry in data["list"]:
                forecast_time = datetime.utcfromtimestamp(entry["dt"])
                for hour, target_time in forecast_hours.items():
                    # Check if forecast time is close to target time
                    if abs((forecast_time - target_time).total_seconds()) <= 5400:  # within a 1.5-hour tolerance
                        forecast_data[hour] = entry["weather"][0]["description"]
                        forcast_id.append(entry["weather"][0]['id'])

            # fill labels and put images
            self.lblforecast_temp1.setText(forecast_data[3])
            self.showForeCastIcon(self.forecast_icon1,forcast_id[0])
            self.lblforecast_temp2.setText(forecast_data[6])
            self.showForeCastIcon(self.forecast_icon2, forcast_id[1])
            self.lblforecast_temp3.setText(forecast_data[9])
            self.showForeCastIcon(self.forecast_icon3, forcast_id[2])
            self.lblforecast_temp4.setText(forecast_data[12])
            self.showForeCastIcon(self.forecast_icon4, forcast_id[3])

        except Exception as e:
            print(e)

    def showForeCastIcon(self,lbl,id):

        try:
            if id >= 200 and id <= 232:  # Thunderstorms
                pixmap = QPixmap("images/09d.png")
                lbl.setPixmap(pixmap)
            elif id >= 300 and id <= 321:  # Drizzle
                pixmap = QPixmap("images/10d.png")
                lbl.setPixmap(pixmap)
            elif id >= 500 and id <= 504:  # Rain
                pixmap = QPixmap("images/10n.png")
                lbl.setPixmap(pixmap)
            elif id == 511:  # freezing Rain
                pixmap = QPixmap("images/09n.png")
                lbl.setPixmap(pixmap)
            elif id >= 520 and id <= 531:  # Rain
                pixmap = QPixmap("images/10d.png")
                lbl.setPixmap(pixmap)
            elif id >= 600 and id <= 622:  # Snow
                pixmap = QPixmap("images/13d.png")
                lbl.setPixmap(pixmap)
            elif id >= 600 and id <= 622:  # Atmosphere
                pixmap = QPixmap("images/03d.png")
                lbl.setPixmap(pixmap)
            elif id == 800:  # Clear
                pixmap = QPixmap("images/01n.png")
                lbl.setPixmap(pixmap)
            elif id == 801 or id == 802:  # few clouds and  scattered clouds
                pixmap = QPixmap("images/02n.png")
                lbl.setPixmap(pixmap)
            elif id == 803 or id == 804:  # overcast clouds and  broken clouds
                pixmap = QPixmap("images/03d.png")
                lbl.setPixmap(pixmap)
        except Exception as e:
            print(e)

    #main window drag funcs
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)