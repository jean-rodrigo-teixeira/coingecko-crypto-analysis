import yfinance as yf
import os

# Define the Bitcoin symbol on Yahoo Finance
symbol = "BTC-USD"

# Define the desired time period
start_date = "2010-01-01"  # Start date
end_date = "2025-01-01"    # End date

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

# Download historical data
try:
    data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
    
    # Save data as CSV
    data.to_csv(csv_path)
    print(f"Data saved at: {csv_path}")
except Exception as e:
    print(f"Error downloading data: {e}")
