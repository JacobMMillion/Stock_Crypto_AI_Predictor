import requests
import json
from dotenv import load_dotenv
import os

"""
Ingest stock data from Alpha Vantage: https://www.alphavantage.co/documentation/
Write to file: `stock_data.json`
"""

# Load the environment variables
load_dotenv()

# Access the API key
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

# output file
file_name = 'stock_data.json'

symbols = ['SPY']  # S&P 500 ETFs

for symbol in symbols:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=full'
    response = requests.get(url)
    data = response.json()

    # write json to file
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

print(f"stock data written to {file_name}")