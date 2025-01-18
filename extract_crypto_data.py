import os
import requests
import pandas as pd
import time
from datetime import datetime

# Getting the output folder from environment variables or setting a default
output_folder = os.getenv('CRYPTO_DATA_PATH', 'crypto_data')

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to get general data and metadata
def get_crypto_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    response = requests.get(url)
    
    # Handle HTTP 429 (Rate Limit Exceeded)
    if response.status_code == 429:
        print(f"Rate limit reached for {coin_id}. Waiting 60 seconds...")
        time.sleep(60)
        response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {coin_id}: Status Code {response.status_code}")
        return None

# Function to get historical price data
def get_historical_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {'vs_currency': 'usd', 'days': '365'}
    response = requests.get(url, params=params)
    
    # Handle HTTP 429 (Rate Limit Exceeded)
    if response.status_code == 429:
        print(f"Rate limit reached for {coin_id}. Waiting 60 seconds...")
        time.sleep(60)
        response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching historical data for {coin_id}: Status Code {response.status_code}")
        return None

# List of coins
coins = ['bitcoin', 'ethereum', 'ripple', 'litecoin']

# Creating lists to store data
id_name_list = []
metadata_list = []
price_data_list = []

# Extracting data for each coin
for i, coin in enumerate(coins, start=1):
    print(f"Extracting data for {coin}...")
    try:
        # Fetch general data for the coin
        data = get_crypto_data(coin)
        if data is None:
            continue
        
        # Fetch historical price data
        historical_data = get_historical_data(coin)
        if historical_data is None:
            continue
        
        # Extracting metadata
        if 'market_data' in data:
            current_price = data['market_data']['current_price']['usd']
            market_cap = data['market_data']['market_cap']['usd']
            total_supply = data['market_data']['total_supply']
            max_supply = data['market_data']['max_supply']
        else:
            current_price = 'No data'
            market_cap = 'No data'
            total_supply = 'No data'
            max_supply = 'No data'
        
        metadata_list.append({
            'ID': i,
            'Coin': coin,
            'Current Price (USD)': current_price,
            'Market Cap (USD)': market_cap,
            'Total Supply': total_supply,
            'Max Supply': max_supply
        })
        
        # Extracting historical prices
        if 'prices' in historical_data and historical_data['prices']:
            for price in historical_data['prices']:
                timestamp = datetime.utcfromtimestamp(price[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                price_value = str(price[1]).replace(',', '.')
                price_data_list.append({
                    'ID': i,
                    'Date': timestamp,
                    'Price (USD)': price_value
                })
        else:
            print(f"No historical data for {coin} or data unavailable.")
        
        # Saving ID and Name
        id_name_list.append({
            'ID': i,
            'Coin': coin
        })

        print(f"Data and metadata for {coin} successfully saved.")
        time.sleep(2)  # Wait 2 seconds before the next request
        
    except KeyError as e:
        print(f"KeyError while accessing data for {coin}: {e}")
    except Exception as e:
        print(f"Unknown error while accessing data for {coin}: {e}")

# Converting lists to DataFrames
id_name_df = pd.DataFrame(id_name_list)
metadata_df = pd.DataFrame(metadata_list)
price_data_df = pd.DataFrame(price_data_list)

# Saving all data to CSV files in the specified folder
id_name_df.to_csv(os.path.join(output_folder, 'crypto_id_and_name.csv'), index=False)
metadata_df.to_csv(os.path.join(output_folder, 'crypto_metadata.csv'), index=False)
price_data_df.to_csv(os.path.join(output_folder, 'crypto_price_data.csv'), index=False)

print(f"All data successfully saved in the folder: {output_folder}")
