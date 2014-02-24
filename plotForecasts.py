
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
    print "Updating at ",datetime.datetime.now()
    wundergnd.updateForecast()

    # Temperature
    times,temps = wundergnd.get_temp_forecast()
    timesfl,feelslike = wundergnd.get_feels_like_temp_forecast()

    # Snowfall
    times_snow,snow   = wundergnd.get_snow_forecast ()
    snow_cum = [0]
    for s in snow:
        snow_cum.append( snow_cum[-1]+s )
    snow_cum.pop(0)

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
    snow_rate_data = {
        'name': "Snowfall rate (in/hour)",
        'x': times_snow,
        'y': snow,
        'line':{'color':'red','thickness':3}
        }
    snow_cum_data = {
        'name': "Cumulative Snowfall (in)",
        'x': times_snow,
        'y': snow_cum,
        'line':{'color':'blue','thickness':3}
        }
    layout_temp = {'title':'Temperature Forecast'}
    layout_snow = {'title':'Snow Forecast'}
    try:
        out=py.plot([temp_data,feels_like_data],filename="TempForecast",
                              fileopt="overwrite",layout=layout_temp,
                              world_readable=True, width=1000, height=650)
        out=py.plot([snow_rate_data,snow_cum_data],filename="SnowForecast",
                              fileopt="overwrite",layout=layout_snow,
                              world_readable=True, width=1000, height=650)
    except:
        print "Connection Error, no update performed at ",datetime.datetime.now()

    # Wait an hour
    print "...complete"
    time.sleep(60*60)










