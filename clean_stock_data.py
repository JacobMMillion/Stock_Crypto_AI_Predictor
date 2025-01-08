from sklearn.model_selection import train_test_split
import json
import pandas as pd

"""
Clean ingested stock data, write out to cleaned_stock_data.csv
"""

# Load the stock data
stock_data = {}

try:
    with open('stock_historical_data.json', 'r') as file:
        stock_data = json.load(file)
except FileNotFoundError:
    print("Stock file not found!")
except json.JSONDecodeError:
    print("Invalid JSON format for stock data!")

# Prepare list to store data
data_list = []

# Process stock data
for symbol, info in stock_data.items():
    meta_data = info.get('Meta Data', {})
    time_series = info.get('Time Series (Daily)', {})

    for date, values in time_series.items():
        data_list.append({
            'symbol': symbol,
            'date': date,
            'open': float(values.get('1. open', 0)),
            'high': float(values.get('2. high', 0)),
            'low': float(values.get('3. low', 0)),
            'close': float(values.get('4. close', 0)),
            'volume': int(values.get('5. volume', 0))
        })

# Convert to DataFrame
stock_df = pd.DataFrame(data_list)

# Save cleaned stock data to CSV
file_name = 'cleaned_stock_data.csv'
stock_df.to_csv(file_name, index=False)

print(f"Stock data cleaned and written to {file_name}!")