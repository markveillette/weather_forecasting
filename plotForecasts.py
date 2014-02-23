
import plotly
import csv
import time
import datetime
from WeatherUndergroundForecast import WeatherUndergroundForecast


# This script will download the lastest forecast data every hour and upload the results to plotly for viewing
KEY_FILE = 'keys/plotly_api_key'
with open(KEY_FILE,'r') as api_key:
    plotly_username = csv.reader(api_key).next()[1]
    plotly_api      = csv.reader(api_key).next()[1]
py = plotly.plotly(plotly_username, plotly_api)


HOME_STATE = 'MA'
HOME_TOWN  = 'Wilmington'

wundergnd = WeatherUndergroundForecast()
wundergnd.get_api_keyi_from_file('keys/weather_underground_api_key')
wundergnd.state = HOME_STATE
wundergnd.town  = HOME_TOWN


while True:
    wundergnd.updateForecast()
    times,temps = wundergnd.get_temp_forecast()
    times,feelslike = wundergnd.get_feels_like_temp_forecast()

    temp_data = {
        'name': "Temperature (F)",
        'x': times,
        'y': temps,
        'line':{'color':'blue','thickness':3}
        }
    feels_like_data = {
        'name': "Feels like (F)",
        'x': times,
        'y': feelslike,
        'line':{'color':'red','thickness':3}
        }
    try:
        out=py.plot([temp_data,feels_like_data],filename="TempForecast",
                              fileopt="overwrite",
                              world_readable=True, width=1000, height=650)
    except:
        print "Connection Error, no update performed at ",datetime.datetime.now()

    # Wait an hour
    time.sleep(60*60)










