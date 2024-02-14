import requests

# fetch resource and convert to json
# data = requests.get('https://catfact.ninja/fact').json()

try:
    response = requests.get('https://catfact.ninja/fact')
    print(response.status_code) # was request successful? 200s are generally a success

    response.raise_for_status() # raise an exception for 400 or 500 code - if raised jump to except block

    print(response.text) # text version of the response
    print(response.json()) # convert to json

    data = response.json()

    fact = data['fact']
    print(f'A random cat fact is {fact}')

except Exception as e:
    print(e)
    print('There was an error making the request.')