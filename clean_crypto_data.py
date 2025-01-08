from sklearn.model_selection import train_test_split
import json
import pandas as pd

"""
Clean ingested crypto data, write out to cleaned_crypto_data.csv
"""

# Load the crypto data
crypto_data = []

try:
    with open('crypto_historical_data.json', 'r') as file:
        # Parse JSON data
        crypto_data = json.load(file)
except FileNotFoundError:
    print("Crypto data file not found!")
except json.JSONDecodeError:
    print("Invalid JSON format for crypto data!")

# Prepare list to store data
data_list = []

# Process crypto data
for entry in crypto_data:
    data_list.append({
        'symbol': entry.get('symbol', ''),
        'name': entry.get('name', ''),
        'date': entry.get('date', ''),
        'current_price': entry.get('current_price', 0.0),
        'market_cap': entry.get('market_cap', 0.0),
        'total_volume': entry.get('total_volume', 0.0)
    })

# Convert to DataFrame
crypto_df = pd.DataFrame(data_list)

# Save cleaned crypto data to CSV
file_name = 'cleaned_crypto_data.csv'
crypto_df.to_csv(file_name, index=False)

print(f"Crypto data cleaned and written to {file_name}!")