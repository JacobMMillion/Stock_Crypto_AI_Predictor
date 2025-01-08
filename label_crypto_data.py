import pandas as pd

# Read the cleaned data CSV
df = pd.read_csv('cleaned_crypto_data.csv')

# Add a new column 'next_day_price' to shift the current price and compare
df['next_day_price'] = df.groupby('symbol')['current_price'].shift(1)

# Create the label column: 1 if price increases the next day, 0 if not
df['label'] = (df['next_day_price'] > df['current_price']).astype(int)

# # Drop the 'next_day_price' column as it's no longer needed
df = df.drop(columns=['next_day_price'])

# Drop the latest row, as this cannot be labeled. We will predict with this row later.
df = df.drop(df.index[0])

# Write the labeled data to a new CSV, maintaining the original order
df.to_csv('labeled_crypto_data.csv', index=False)

print("Labels added and data saved to 'labeled_crypto_data.csv'")