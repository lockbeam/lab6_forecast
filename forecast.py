# example URL
# https://api.openweathermap.org/data/2.5/forecast?q=minneapolis,mn,us&units=imperial&appid=ba5b32653d02c5fa8fc7729446147f8b

import os
import requests
from pprint import pprint
from datetime import datetime

key = os.environ.get('WEATHER_KEY')
url = 'https://api.openweathermap.org/data/2.5/forecast'

def main():
    location = get_location()
    weather_data, error = get_current_weather(location, key)
    if error:
        print('Sorry, could not get the weather')
    else:
        get_temp(weather_data)

def get_location():
    city, country = '', ''
    
    while len(city) == 0:
        city = input('What city do you want the temp of? ').strip()
    
    while len(country) != 2 or not country.isalpha():
        country = input('What country is that city in using the two letter country code? ').strip()

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
        print(e)
        print(response.text) # for debugging as needed
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
            print(f'On {forecast_date} the weather is forecasted to be: \nTemperature: {temp}\nWind Speed: {wind_speed}\nDescription: {weather_description}\n')
    except KeyError:
        print('This data is not in the format expected')
    
if __name__ == '__main__':
    main()

