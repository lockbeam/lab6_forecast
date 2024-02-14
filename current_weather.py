import requests
from pprint import pprint
import os

key = os.environ.get('WEATHER_KEY')
# print(key) # validation during development

# old way with f string
# url = f'https://api.openweathermap.org/data/2.5/weather?q=minneapolis,mn,us&units=imperial&appid={key}'

url = 'https://api.openweathermap.org/data/2.5/weather'

def main():
    location = get_location()
    weather_data, error = get_current_weather(location, key)
    if error:
        print('Sorry, could not get the weather')
    else:
        current_temp = get_temp(weather_data)
        print(f'The current temperature is {current_temp} in F')

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
        temp = weather_data['main']['temp']
        return temp
    except KeyError:
        print('This data is not in the format expected')
        return 'Unknown'
    
if __name__ == '__main__':
    main()
