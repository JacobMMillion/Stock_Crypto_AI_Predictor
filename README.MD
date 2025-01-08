# Stock and Crypto Price Prediction Pipeline

This program ingests historical stock and cryptocurrency data, then trains a model to predict whether the next day will result in a price increase.

## Pipeline Overview

### 1) Ingesting Data
The first step involves ingesting historical price data for stocks and cryptocurrencies. This is done with the following scripts:
- `ingest_crypto_data.py` – Writes to file: `stock_historical_data.json`
- `ingest_stock_data.py` – Writes to file: `crypto_historical_data.json`

The data is obtained from the APIs of the following sources:
- **Stocks**: Alpha Vantage (25 API calls / day) – [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)
- **Cryptocurrencies**: CoinGecko (10000 API calls / month, or 333 / day) – [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

### 2) Cleaning Data
After ingestion, the historical data for both stocks and cryptocurrencies is stored in their respective files in JSON format. These files are then processed and cleaned by the following scripts:
- `clean_crypto_data.py` – Writes to file: `cleaned_crypto_data.csv`
- `clean_stock_data.py` – Writes to file: `cleaned_stock_data.csv`

### 3) Add Labels to Data
We now add labels to the cleaned data for training the model. This is done with the following scripts:
- `label_crypto_data.py` – Writes to file: `labeled_crypto_data.json`
- `label_stock_data.py` – Writes to file: `labeled_stock_data.json`

The first row of each of the cleaned data is dropped in the new files, as it cannot be labeled.
This labeled data will then be used for training in the next step. The label is `1` if the price of
the stock or cryptocurrency rose the following day, and `0` otherwise.

### 4) Train Model  
The model is trained using the cleaned and labeled data, with the dataset split into training and testing sets. A **Random Forest Classifier** from `sklearn` is used to predict price movement. 

The model is initially defined with general hyperparameters, and then optimized using **GridSearchCV** to find the best combination of parameters like the number of trees, tree depth, and minimum samples for splitting. The training set is used to fit the model, with features such as price, market cap, and volume, and the target label indicating price movement (increase or decrease).

### 5) Test and Make Predictions  
Once trained, the model is evaluated on the test set using performance metrics like **precision**, **accuracy**, **recall**, and **F1-score**. These metrics provide insights into the model's ability to predict price movement. After evaluation, the model can be used to predict whether the price will increase the following day, based on current market features.

Once the model is trained, it is used to make predictions on the test set. Model performance is evaluated using metrics such as **accuracy**, **precision**, **recall**, and **F1-score**. These metrics provide insight into how well the model predicts the next day's price movement.

After evaluating the model, it can be used to predict whether the price of a cryptocurrency will increase the next day by feeding the model new features for the current day.