import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
file_path = 'cleaned_crypto_data.csv'
file_path2 = 'cleaned_stock_data.csv'

# Read the CSV file
df = pd.read_csv(file_path)
df2 = pd.read_csv(file_path2)

# Set options to display everything
# pd.set_option('display.max_rows', None)        # Show all rows
# pd.set_option('display.max_columns', None)     # Show all columns
# pd.set_option('display.width', None)           # Auto-adjust width to avoid truncation
# pd.set_option('display.max_colwidth', None)    # Show full content of each column

pd.set_option('display.float_format', '{:.6f}'.format)  # Show 6 decimal places

# Print the DataFrame
print("Cryptocurrency Current Prices:")
print(df)
print("------------------------------------------------------------------")
print("")

print("Stock Historical Prices (SPY and BAR):")
print(df2)
print("------------------------------------------------------------------")

# Reset options (optional if you don't want to keep these settings globally)
# pd.reset_option('display.max_rows')
# pd.reset_option('display.max_columns')
# pd.reset_option('display.width')
# pd.reset_option('display.max_colwidth')