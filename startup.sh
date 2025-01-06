#!/bin/bash

MINUTES_TO_SLEEP=5
sleep_delay=$((MINUTES_TO_SLEEP * 60))

while true; do 
    
    echo "begining to update data..."

    # ingest updatd data from coinmarketcap api
    python3 ingest_crypto_data.py

    # ingest updated stock data
    python3 ingest_stock_data.py

    # modify data to get the attributes we care about

    # make calculations as needed

    # analyze the data, use AI to make predictions in key moments, critical lines
    # this could involve searching to see if there is news abt anything
    # idea is to get and be informed

    # send an email
    # python3 send_email.py

    # sleep for a specific duration to prevent high CPU usage
    echo "pausing to save cpu usage"
    sleep $sleep_delay
    echo "waking up from sleeping"

done