# example URL
# https://api.openweathermap.org/data/2.5/forecast?q=minneapolis,mn,us&units=imperial&appid=ba5b32653d02c5fa8fc7729446147f8b

import os
import requests
from pprint import pprint
from datetime import datetime
import logging

# Configure your logger. filename - where to write to. otherwise logs write to the console
# level is the minimum log level that is recorded. DEBUG means log everything. 
# format sets the format of the string that is recorder for each log event. 
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')

key = os.environ.get('WEATHER_KEY')
if not key:
    logging.debug(f'Problem connecting to key')
url = 'https://api.openweathermap.org/data/2.5/forecast'

def main():
    location = get_location()
    weather_data, error = get_current_weather(location, key)
    if error:
        print('Sorry, could not get the weather')
        logging.debug(f'Error retrieving weather data due to {error}')
    else:
        get_temp(weather_data)

def get_location():
    city, country = '', ''
    
    while len(city) == 0:
        city = input('What city do you want the temp of? ').strip()
        logging.info(f'User inputted {city} for city')
    
    while len(country) != 2 or not country.isalpha():
        country = input('What country is that city in using the two letter country code? ').strip()
        logging.info(f'User inputted {country} for country')


    location = f'{city},{country}'
    return location

def get_current_weather(location, key): 
    try:
        query = {'q': location, 
                'units': 'imperial', 
                'appid': key}
        response = requests.get(url, params=query)
        response.raise_for_status() # raise exception for 400 or 500 errors
        data = response.json() # may error if response not JSON
        return data, None # return data and NO error
    except Exception as e:
        logging.exception(f'Error requesting {e}')
        logging.exception(response.text) # for debugging as needed
        return None, e # return NO data and error
    
def get_temp(weather_data):
    try:
        list_of_forecasts = weather_data['list']
        for forecast in list_of_forecasts:
            temp = forecast['main']['temp']
            timestamp = forecast['dt']
            weather_description = forecast['weather'][0]['description']
            wind_speed = forecast['wind']['speed']
            forecast_date = datetime.fromtimestamp(timestamp)
            print(f'On {forecast_date} in your local time the weather is forecasted to be: \nTemperature: {temp}\nWind Speed: {wind_speed}\nDescription: {weather_description}\n')
        logging.info('Successfully executed full program')
    except KeyError:
        logging.info('This data is not in the format expected')
    
if __name__ == '__main__':
    main()

