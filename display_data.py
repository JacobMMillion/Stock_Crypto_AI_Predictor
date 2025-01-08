import pandas as pd
from datetime import datetime, timedelta
import time

# Replace 'your_file.csv' with the path to your CSV file
file_path = 'labeled_crypto_data.csv'
file_path2 = 'labeled_stock_data.csv'

# Read the CSV file
df = pd.read_csv(file_path)
df2 = pd.read_csv(file_path2)

"""
Can adjust as needed, just make sure to reset at the end of the script
as to not affect anything globally
"""
# Set options to display everything
# pd.set_option('display.max_rows', None)        # Show all rows
# pd.set_option('display.max_columns', None)     # Show all columns
# pd.set_option('display.width', None)           # Auto-adjust width to avoid truncation
# pd.set_option('display.max_colwidth', None)    # Show full content of each column

pd.set_option('display.float_format', '{:.6f}'.format)  # Show 6 decimal places

time = datetime.today()

# Print the DataFrame
print("------------------------------------------------------------------")
print("Values below accurate as of", time)
print("------------------------------------------------------------------")
print("Bitcoin Historical Prices (1 year):")
print(df)
print("------------------------------------------------------------------")
print("Stock Historical Prices (S&P):")
print(df2)
print("------------------------------------------------------------------")
print("")