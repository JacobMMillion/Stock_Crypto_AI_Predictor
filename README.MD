# Stock and Crypto Price Prediction Pipeline

This program ingests historical stock and cryptocurrency data, processes and labels it, and then trains a machine learning model to predict whether the next day's price will increase.

## Pipeline Overview

### 1) Ingesting Data
The first step involves ingesting historical price data for stocks and cryptocurrencies. This is done with the following scripts:
- `ingest_crypto_data.py` – Writes to file: `crypto_historical_data.json`
- `ingest_stock_data.py` – Writes to file: `stock_historical_data.json`

The data is obtained from the APIs of the following sources:
- **Stocks**: Alpha Vantage (25 API calls / day) – [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)
- **Cryptocurrencies**: CoinGecko (10,000 API calls / month, or 333 / day) – [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

---

### 2) Cleaning Data
After ingestion, the historical data for both stocks and cryptocurrencies is stored in JSON files. These files are then processed and cleaned by the following scripts:
- `clean_crypto_data.py` – Writes to file: `cleaned_crypto_data.csv`
- `clean_stock_data.py` – Writes to file: `cleaned_stock_data.csv`

---

### 3) Adding Labels to Data
Labels are added to the cleaned data to train the model. The label is `1` if the price rose the following day and `0` otherwise. This is done using:
- `label_crypto_data.py` – Writes to file: `labeled_crypto_data.json`
- `label_stock_data.py` – Writes to file: `labeled_stock_data.json`

The first row of each dataset is excluded as it cannot be labeled.

---

### 4) Training the Model
The model is trained using the cleaned and labeled data. A **Random Forest Classifier** from `sklearn` is used to predict price movements. Key steps include:
- Splitting the dataset into training and testing sets.
- Optimizing model hyperparameters using **GridSearchCV**.
- Training on features such as price, market cap, and volume, with the target label indicating price movement.

---

### 5) Testing and Predictions
The trained model is evaluated on the test set using performance metrics like:
- **Accuracy**
- **Precision**
- **Recall**
- **F1-score**

The model can then be used to predict price movement based on new data features.

---

## Automating the Pipeline

To automate the pipeline and run it twice daily, use the provided shell script `run_main.sh`. This script automates the entire process, including ingestion, cleaning, labeling, debugging, and training.

### Usage of `run_main.sh`
1. Ensure all required Python scripts and dependencies are available in the project directory.
2. Make the script executable:
   ```bash
   chmod +x run_main.sh