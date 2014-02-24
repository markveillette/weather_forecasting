import requests
import csv
from datetime import datetime

WUNDERGROUND_URL = "http://api.wunderground.com/api/{api}/hourly10day/q/{state}/{town}.json"

class UnInitError(RuntimeError):
    def __init__(self, arg):
        self.args = arg

# Class which downloads 10 day forecast from weather underground
class WeatherUndergroundForecast(object):
    def __init__(self):
        self.has_forecast = False
        self.forecast_time = ''
        self.api_key = "UNSET"
        self.state = "UNSET"
        self.town = "UNSET"
        self._current_forecast_data = []

    def get_api_keyi_from_file(self,fileName):
        with open(fileName,'r') as api_key_file:
            self.api_key = csv.reader(api_key_file).next()[1]

    # Gets latest forecast
    def updateForecast(self):
        if self.api_key == "UNSET" :
            raise UnInitError("No API key set")
        if self.state == "UNSET" or self.town == "UNSET" :
            raise UnInitError("State and/or Town not set")

        r = requests.get(WUNDERGROUND_URL.format(api=self.api_key,state=self.state,town=self.town))
        self._current_forecast_data = r.json()

        if self._current_forecast_data['response'].has_key('error') :
            print 'ERROR: ',self._current_forecast_data['response']['error']['type']
            print self._current_forecast_data['response']['error']['description']
            self.has_forecast = False
        else:
            self.has_forecast = True
            self.forecast_time = datetime.now()

    def get_forecast_data(self,key):
        if not self.has_forecast:
            raise UnInitError(['No forecast data, plase update forecast'])
        times = []
        vals  = []
        for fcst in self._current_forecast_data['hourly_forecast']:
            times.append( datetime.fromtimestamp( int(fcst['FCTTIME']['epoch']) ) )
            vals.append( fcst[key] )
        return times,vals


    # Methods to get inidividual forecasts
    def get_temp_forecast(self):
        times,temp_dicts = self.get_forecast_data('temp')
        temps = []
        for d in temp_dicts:
            try:
                temps.append( float(d['english']) )
            except ValueError:
                temps.append(float('nan'))
        return times,temps


    def get_feels_like_temp_forecast(self):
        times,temp_dicts = self.get_forecast_data('feelslike')
        temps = []
        for d in temp_dicts:
            try:
                temps.append( float(d['english']) )
            except ValueError:
                temps.append(float('nan'))
        return times,temps

    def get_snow_forecast(self):
        times,snow_dict =  self.get_forecast_data('snow')
        snow = []
        for d in snow_dict:
            try:
                snow.append(float(d['english']))
            except:
                snow.append(0)
        return times,snow

    def get_pop_forecast(self):
        times,pop_str = self.get_forecast_data('pop')
        pop = []
        for p in pop_str:
            try:
                pop.append(float(p))
            except ValueError:
                pop.append(0)
        return times,pop





