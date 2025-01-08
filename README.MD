# Stock and Crypto Price Prediction Pipeline

This program ingests historical stock and cryptocurrency data, then trains a model to predict whether the next day will result in a price increase.

## Pipeline Overview

### 1) Ingesting Data
The first step involves ingesting historical price data for stocks and cryptocurrencies. This is done with the following scripts:
- `ingest_crypto_data.py` – Writes to file: `stock_historical_data.json`
- `ingest_stock_data.py` – Writes to file: `crypto_historical_data.json`

The data is obtained from the APIs of the following sources:
- **Stocks**: Alpha Vantage – [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)
- **Cryptocurrencies**: CoinGecko – [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

### 2) Cleaning Data
After ingestion, the historical data for both stocks and cryptocurrencies is stored in their respective files in JSON format. These files are then processed and cleaned by the following scripts:
- `clean_crypto_data.py` – Writes to file: `cleaned_crypto_data.csv`
- `clean_stock_data.py` – Writes to file: `cleaned_stock_data.csv`

### 3) Add Labels to Data
**TODO:** Add labels to the cleaned data for training the model.

### 4) Train Model
**TODO:** Train a machine learning model using the cleaned and labeled data.

### 5) Test and Make Predictions
**TODO:** Test the trained model and make predictions on whether the next day will see a price increase.