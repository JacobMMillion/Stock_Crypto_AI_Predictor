from sklearn.model_selection import train_test_split
import json
import pandas as pd

"""
Clean ingested stock data, write out to cleaned_stock_data.csv
"""

# Load the stock data
stock_data = ""

try:
    with open('stock_historical_data.json', 'r') as file:
        stock_data = json.load(file)
except FileNotFoundError:
    print("Stock file not found!")
except json.JSONDecodeError:
    print("Invalid JSON format for stock data!")

# Prepare dictionary to store data
stocks_data = {}

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

# Convert to DataFrame
stock_df = pd.DataFrame.from_dict(stocks_data, orient='index')

# Save cleaned stock data to CSV
file_name = 'cleaned_stock_data.csv'
stock_df.to_csv(file_name, index=True)

print(f"Stock data cleaned and written to {file_name}!")
