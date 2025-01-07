#!/bin/bash

# This script automates the process of:
# - Updating crypto data every 5 minutes from the CoinMarketCap API
# - Updating stock data every hour from the Alpha Vantage API
# It continuously runs in a loop, performing the following steps at regular intervals:
# - Fetching current data (crypto every 5 minutes, stocks every hour)
# - Cleaning and organizing the data
# - Analyzing the data and potentially training models for predictions
# - Sending email notifications based on the analysis
#
# The loop runs indefinitely, with sleep intervals to reduce CPU usage.

MINUTES_TO_SLEEP=5     # Crypto update interval (5 minutes)
STOCK_UPDATE_INTERVAL=60   # Stock update interval (60 minutes)

sleep_delay=$((MINUTES_TO_SLEEP * 60))  # Sleep for 5 minutes between each loop

last_stock_update=$(date +%s)  # Track the last update time for stocks

while true; do 
    current_time=$(date +%s)
    echo "Beginning to update data..."

    # Update crypto data (every 5 minutes)
    echo "Updating crypto data..."
    # Ingest current data from CoinMarketCap API
    python3 ingest_crypto_data.py
    # Clean the crypto data
    python3 clean_crypto_data.py

    # Check if it's time to update stocks (every 60 minutes)
    if (( (current_time - last_stock_update) >= STOCK_UPDATE_INTERVAL * 60 )); then
        echo "Updating stock data..."
        # Ingest historical and current stock data from Alpha Vantage API
        python3 ingest_stock_data.py
        # Clean the stock data
        python3 clean_stock_data.py
        last_stock_update=$current_time  # Update the last stock update time
    fi

    # Analyze the data and make predictions (optional)
    # python3 analyze_data.py   # Example of an AI-based analysis script (optional)

    # Send an email based on analysis
    # python3 send_email.py

    # Sleep for 5 minutes before next iteration
    echo "Pausing to save CPU usage"
    sleep $sleep_delay
    echo "Waking up from sleeping"
    echo ""

done