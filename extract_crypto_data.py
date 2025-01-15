import requests
import pandas as pd
from datetime import datetime

# Função para pegar dados históricos
def get_historical_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {'vs_currency': 'usd', 'days': '365'}  # Dados dos últimos 365 dias
    response = requests.get(url, params=params)
    return response.json()

# Dados históricos de Bitcoin
btc_data = get_historical_data('bitcoin')
eth_data = get_historical_data('ethereum')

# Convertendo os timestamps em datas
btc_df = pd.DataFrame(btc_data['prices'], columns=['Timestamp', 'Price'])
btc_df['Date'] = pd.to_datetime(btc_df['Timestamp'], unit='ms')

eth_df = pd.DataFrame(eth_data['prices'], columns=['Timestamp', 'Price'])
eth_df['Date'] = pd.to_datetime(eth_df['Timestamp'], unit='ms')

# Selecionando apenas a coluna de Data e Preço
btc_df = btc_df[['Date', 'Price']]
eth_df = eth_df[['Date', 'Price']]

# Salvando os dados em um arquivo Excel
with pd.ExcelWriter('crypto_data.xlsx') as writer:
    btc_df.to_excel(writer, sheet_name='Bitcoin', index=False)
    eth_df.to_excel(writer, sheet_name='Ethereum', index=False)

print("Dados salvos com sucesso no arquivo 'crypto_data.xlsx'.")
