import os
import json
import requests
from dotenv import load_dotenv

"""
Ingest stock data from Alpha Vantage: https://www.alphavantage.co/documentation/
Write to file: `stock_data.json`
"""

# Load the environment variables
load_dotenv()

# Access the API key
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

# output file
file_name = 'stock_historical_data.json'

# Symbols for stock data
symbols = ['SPY', 'BAR']  # S&P 500 ETF and GOLD

# Create a dictionary to hold all data
all_data = {}

for symbol in symbols:

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=full'
    response = requests.get(url)
    data = response.json()

    # Add the symbol data to the dictionary
    all_data[symbol] = data

# Write the full dictionary to the JSON file
with open(file_name, 'w') as file:
    json.dump(all_data, file, indent=4)

print(f"Stock data written to {file_name}")