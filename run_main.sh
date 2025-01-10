#!/bin/bash

# Script Name: run_main.sh
#
# Description: 
# This script automates the execution of a series of Python scripts for data 
# ingestion, cleaning, labeling, debugging, and model training. The tasks are 
# executed twice a day with a 12-hour interval between each execution. 
# 
# Steps Per Execution:
# 1. Ingest data for cryptocurrencies and stocks.
# 2. Clean the ingested data.
# 3. Add labels to the cleaned data.
# 4. Display data for debugging purposes.
# 5. Train models and predict prices for the next day.
#
# Usage:
# 1. Save this script as `run_main.sh`.
# 2. Make it executable: chmod +x run_tasks_twice.sh
# 3. Run it manually: ./run_tasks_twice.sh
# 
# Note: This script will execute twice and then terminate. To run daily, schedule
# it via a cron job or another scheduler.

# Function to run the tasks
run_tasks() {
    echo "Starting tasks at $(date)"

    # Ingest data
    python3 ingest_crypto_data.py
    python3 ingest_stock_data.py

    # Clean data
    python3 clean_crypto_data.py
    python3 clean_stock_data.py

    # Add labels
    python3 label_crypto_data.py
    python3 label_stock_data.py

    # Display data for debugging
    python3 display_data.py

    # Train model and predict price for the next day
    python3 train_crypto_model.py
    python3 train_stock_model.py

    echo "Tasks completed at $(date)"
    echo "--------------------------------------------"
}

# Loop to run twice a day
for i in {1..2}; do
    run_tasks
    if [ "$i" -lt 2 ]; then
        # Sleep for 12 hours (12 hours * 60 minutes * 60 seconds)
        sleep 43200
    fi
done