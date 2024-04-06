import requests
from datetime import date, timedelta, datetime
from dateutil import tz


class Weather:

    def __init__(self, city):
        self.day = []
        self.city = city
        self.status = self.get_weather()
        self.download_day_temp = None

    def get_weather(self):
        API_KEY = '5cb00ebacb888af1ed92bedb4ce335d7'

        url_30 = f'https://pro.openweathermap.org/data/2.5/forecast/climate?q={self.city}&units=metric&appid={API_KEY}'
        res_30 = requests.get(url_30)

        url_now = f'https://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&appid={API_KEY}'
        res_now = requests.get(url_now)

        presentday = date.today()
        res_dict = res_30.json()
        res_dict_now = res_now.json()
        print(res_dict_now["main"]["temp"])
        self.download_day_temp = res_dict_now["main"]["temp"]

        for i in range(0, len(res_dict["list"])):

            self.day.append(Day(str(presentday + timedelta(i)),
                                res_dict["list"][i]["temp"]["day"],
                                res_dict["list"][i]["temp"]["min"],
                                res_dict["list"][i]["temp"]["max"],
                                res_dict["list"][i]["weather"][0]["icon"],
                                res_dict["list"][i]["pressure"],
                                res_dict["list"][i]["humidity"],
                                res_dict["list"][i]["weather"][0]["description"],
                                res_dict["list"][i]["sunrise"],
                                res_dict["list"][i]["sunset"],
                                res_dict["list"][i]["speed"]))

        return res_30

    def refresh(self):
        self.day.clear()
        self.get_weather()


class Day:

    def __init__(self, date, temperature_avg, temperature_min, temperature_max, overall_icon, pressure, humidity,
                 description, sunrise,
                 sunset, wind_speed):
        self.date = date
        self.temperature_avg = temperature_avg
        self.temperature_min = temperature_min
        self.temperature_max = temperature_max
        self.overall_icon = overall_icon
        self.pressure = pressure
        self.humidity = humidity
        self.description = description
        self.sunrise_utc = datetime.utcfromtimestamp(sunrise).replace(tzinfo=tz.tzutc())
        self.sunset_utc = datetime.utcfromtimestamp(sunset).replace(tzinfo=tz.tzutc())
        self.wind_speed = wind_speed
        self.sunrise = self.sunrise_utc.astimezone(tz.tzlocal()).strftime('%H:%M')
        self.sunset = self.sunset_utc.astimezone(tz.tzlocal()).strftime('%H:%M')
