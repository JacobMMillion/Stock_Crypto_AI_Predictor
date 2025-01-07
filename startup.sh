#!/bin/bash

# This script has a loop that runs once every hour
# The free API for Alpha Vantage is limited to 25 / day
# We can keep crypto more up to date by pipelining and running crypto ingestion more frequently

MINUTES_TO_SLEEP=60
sleep_delay=$((MINUTES_TO_SLEEP * 60))

while true; do 
    
    echo "begining to update data..."

    # ingest current data from coinmarketcap api
    python3 ingest_crypto_data.py

    # ingest historical and current stock data from Alpha Vantage api
    python3 ingest_stock_data.py

    # modify data to get the attributes we care about
    # we have more to work with for the stock data, so we work with this closely first
    python3 clean_all_data.py

    # analyze the data, use AI to make predictions in key moments, critical lines
    # this could involve searching to see if there is news abt anything
    # idea is to get and be informed

    # TRAIN A MODEL TO PREDICT THE STOCK WITH THE HIGHEST PROBABILITY OF GAINING IN THE NEXT TRADING DAY

    # send an email, determine if should be sent
    python3 send_email.py

    # sleep for a specific duration to prevent high CPU usage
    echo "pausing to save cpu usage"
    sleep $sleep_delay
    echo "waking up from sleeping"
    echo ""

done