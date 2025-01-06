from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import load_dotenv
import os

"""
Ingest crypto data from Coin Market Cap: https://coinmarketcap.com/api/documentation/v1/#
Write to file: `crypto_data.json`
"""

print("ingesting data...")

# Load the environment variables
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')

# output file
file_name = 'cypto_data.json'

url = 'http://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


# write json to file
with open(file_name, 'w') as file:
    json.dump(data, file, indent=4)

print(f"crypto data written to {file_name}")