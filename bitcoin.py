import requests
from pprint import pprint
# pretty print

coindesk_url = 'http://api.coindesk.com/v1/bpi/currentprice.json'

response = requests.get(coindesk_url)
data = response.json()
# pprint(data)

dollars_exchange_rate = data['bpi']['USD']['rate_float']
print(dollars_exchange_rate)

bitcoin = float(input('Enter the number of bitcoin you have: '))

bitcoin_value_in_dollars = bitcoin * dollars_exchange_rate

print(f'{bitcoin} Bitcoin is worth ${bitcoin_value_in_dollars}')
