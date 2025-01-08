from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import time

"""
Ingest historical crypto data from CoinGecko
Write to file: `crypto_historical_data.json`
"""

# Load the environment variables
load_dotenv()

# Output file
file_name = 'crypto_historical_data.json'
api_key = os.getenv('COINGECKO_API_KEY')

# Function to fetch historical price data from CoinGecko API
def get_historical_price(crypto_id, date):

    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/history"

    parameters = {
        "date": date,  # Format: dd-mm-yyyy
        "localization": "false"
    }

    session = Session()

    try:

        response = session.get(url, params=parameters)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.json().get('error', 'Unknown error')}")
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

# Function to get relevant data (symbol, name, market data) for the past 365 days
def get_data(crypto_id):

    end_date = datetime.today()
    crypto_data = []
    difference = 365

    # Load the current crypto data
    try:
        with open(file_name, 'r') as file:
            # Parse JSON data
            crypto_data = json.load(file)
    except FileNotFoundError:
        print("Crypto data file not found!")
    except json.JSONDecodeError:
        print("Invalid JSON format for crypto data!")

    # Check if there is data and access the first entry's date
    if crypto_data:
        first_entry = crypto_data[0]  # Get the first entry
        first_date_str = first_entry.get('date', '')  # Extract the date as a string
        
        if first_date_str:
            # Convert the string to a datetime object
            first_date = datetime.strptime(first_date_str, "%d-%m-%Y")
            
            # Get the current date
            current_date = datetime.now()
            
            # Calculate the difference in days
            difference = (current_date - first_date).days
            print(f"The difference in days between {first_date_str} and today is: {difference} days")
        else:
            print("Crypto ingestion date is missing in the first entry!")
    else:
        print("No crypto historical data found, obtaining a year of data!")
        difference = 365

    # Get the new data if needed
    new_data = []
    for i in range(difference):

        date = (end_date - timedelta(days=i)).strftime('%d-%m-%Y')
        print(f"Fetching data for {date}...")

        result = get_historical_price(crypto_id, date)

        if result:

            coin_data = {
                'symbol': result['symbol'],  # Coin symbol (e.g., BTC)
                'name': result['name'],  # Coin name (e.g., Bitcoin)
                'date': date,
                'current_price': result['market_data']['current_price']['usd'],  # Market data (prices, volume, etc.)
                'market_cap': result['market_data']['market_cap']['usd'],
                'total_volume': result['market_data']['total_volume']['usd']
            }

            new_data.append(coin_data)

            print(f"Appended data for {date} to new_data!")

        # IMPORTANT: we sleep here as to not exceed API request limits and error out
        time.sleep(13)

    # Append the new data into the existing crypto data
    if new_data:

        crypto_data = new_data + crypto_data  # Prepend the new data to the existing list

        # Write the updated data to the file
        with open(file_name, 'w') as file:
            json.dump(crypto_data, file, indent=4)

        print(f"Crypto data written to {file_name}!")

# MAIN
crypto_id = "bitcoin"  # Can get data for other coins as well in this way
get_data(crypto_id)
print(f"Crypto data ingested and written to {file_name}!")