from sklearn.model_selection import train_test_split
import json
import pandas as pd
import numpy as np

# Load the stock data
stock_data = ""
crypto_data = ""

try:
    with open('stock_historical_data.json', 'r') as file:
        stock_data = json.load(file)
except FileNotFoundError:
    print("Stock file not found!")
except json.JSONDecodeError:
    print("Invalid JSON format for stock data!")

try:
    with open('crypto_live_data.json', 'r') as file:
        crypto_data = json.load(file)
except FileNotFoundError:
    print("Crypto file not found!")
except json.JSONDecodeError:
    print("Invalid JSON format for crypto data!")

# Prepare dictionaries to store data
stocks_data = {}
crypto_data_cleaned = {}

# Process stock data
for symbol, info in stock_data.items():
    time_series = info.get('Time Series (Daily)', {})
    stock_columns = {}

    for date, vals in time_series.items():
        stock_columns[f'{date}_open'] = float(vals.get('1. open', 0))
        stock_columns[f'{date}_high'] = float(vals.get('2. high', 0))
        stock_columns[f'{date}_low'] = float(vals.get('3. low', 0))
        stock_columns[f'{date}_close'] = float(vals.get('4. close', 0))
        stock_columns[f'{date}_volume'] = int(vals.get('5. volume', 0))

    stocks_data[symbol] = stock_columns

# Process crypto data
for crypto in crypto_data.get('data', []):

    symbol = crypto.get('symbol', 'Unknown')
    id = crypto.get('id', -1)
    name = crypto.get('name', 'Unknown')
    quote = crypto.get('quote', {}).get('USD', {})

    crypto_data_cleaned[id] = {
        'symbol': symbol,
        'name': name,
        'price': quote.get('price', 0),
        'volume_24h': quote.get('volume_24h', 0),
        'market_cap': quote.get('market_cap', 0),
        'percent_change_1h': quote.get('percent_change_1h', 0),
        'percent_change_24h': quote.get('percent_change_24h', 0),
        'percent_change_7d': quote.get('percent_change_7d', 0),
        'percent_change_30d': quote.get('percent_change_30d', 0),
        'percent_change_60d': quote.get('percent_change_60d', 0),
        'percent_change_90d': quote.get('percent_change_90d', 0)
    }

# Convert to DataFrames
stock_df = pd.DataFrame.from_dict(stocks_data, orient='index')

crypto_df = pd.DataFrame.from_dict(crypto_data_cleaned, orient='index')
crypto_df['market_cap'] = pd.to_numeric(crypto_df['market_cap'])
crypto_df = crypto_df.sort_values(by='market_cap', ascending=False)

# Print the results
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.width', 10000)  # Avoid line wrapping

# save to data
stock_df.to_csv('cleaned_stock_data.csv', index=True)
crypto_df.to_csv('cleaned_crypto_data.csv', index=False)

print("stock and crypto data cleaned!")