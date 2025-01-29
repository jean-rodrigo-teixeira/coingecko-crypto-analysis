import yfinance as yf
import os
from datetime import datetime
import pandas as pd

# Define the symbols for the top 10 cryptocurrencies on Yahoo Finance
symbols = ["BTC-USD", "ETH-USD", "XRP-USD", "LTC-USD", "ADA-USD", "DOGE-USD", "BNB-USD", "SOL-USD", "MATIC-USD", "DOT-USD"]

# Define the desired time period
start_date = "2010-01-01"  # Start date
end_date = datetime.today().strftime('%Y-%m-%d')  # End date as the current date

# Get the path from the CRYPTO_DATA_PATH environment variable
crypto_data_path = os.getenv("CRYPTO_DATA_PATH")

# If the variable is not set, raise an error
if not crypto_data_path:
    raise EnvironmentError("The environment variable 'CRYPTO_DATA_PATH' is not set.")

# Check if the path exists; if not, create the folder
if not os.path.exists(crypto_data_path):
    os.makedirs(crypto_data_path)

# Define the full path to save the file
csv_path = os.path.join(crypto_data_path, "crypto_price_data.csv")

# List to store the data for each cryptocurrency
all_data = []

# Function to download and process data for each cryptocurrency
def download_and_process_data(symbol):
    try:
        # Download the historical data
        data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
        
        # Reset the index to make sure Date is a column
        data.reset_index(inplace=True)
        
        # Rename the columns to match the desired format
        data.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
        
        # Add the 'Crypto' column with the symbol value
        data.insert(0, 'Crypto', symbol)
        
        # Append the data to the list
        all_data.append(data)
        print(f"Data for {symbol} processed successfully.")
    except Exception as e:
        print(f"Error downloading data for {symbol}: {e}")

# Download and process data for each cryptocurrency in the list
for symbol in symbols:
    download_and_process_data(symbol)

# Concatenate all the data into a single DataFrame
combined_data = pd.concat(all_data, ignore_index=True)

# Save the combined data to a single CSV file
combined_data.to_csv(csv_path, index=False)
print(f"Combined data saved at: {csv_path}")
