import json
import pandas as pd

# Load the crypto data
crypto_data = ""

try:
    with open('crypto_live_data.json', 'r') as file:
        crypto_data = json.load(file)
except FileNotFoundError:
    print("Crypto file not found!")
except json.JSONDecodeError:
    print("Invalid JSON format for crypto data!")

# Prepare dictionary to store cleaned crypto data
crypto_data_cleaned = {}

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

# Convert to DataFrame
crypto_df = pd.DataFrame.from_dict(crypto_data_cleaned, orient='index')
crypto_df['market_cap'] = pd.to_numeric(crypto_df['market_cap'])
crypto_df = crypto_df.sort_values(by='market_cap', ascending=False)

# Save cleaned crypto data to CSV
file_name = 'cleaned_crypto_data.csv'

crypto_df.to_csv(file_name, index=False)

print(f"Crypto data cleaned and written to {file_name}!")