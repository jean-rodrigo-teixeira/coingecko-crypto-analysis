import yfinance as yf
import os
from datetime import datetime
import pandas as pd

# Define os símbolos do Bitcoin e Ethereum no Yahoo Finance
symbols = ["BTC-USD", "ETH-USD"]

# Define o período de tempo desejado
start_date = "2010-01-01"  # Data de início
end_date = datetime.today().strftime('%Y-%m-%d')  # Data final como a data atual

# Obtém o caminho da variável de ambiente CRYPTO_DATA_PATH
crypto_data_path = os.getenv("CRYPTO_DATA_PATH")

# Se a variável não estiver definida, lança um erro
if not crypto_data_path:
    raise EnvironmentError("The environment variable 'CRYPTO_DATA_PATH' is not set.")

# Verifica se o caminho existe; se não, cria a pasta
if not os.path.exists(crypto_data_path):
    os.makedirs(crypto_data_path)

# Define o caminho completo para salvar o arquivo
csv_path = os.path.join(crypto_data_path, "crypto_price_data.csv")

# Lista para armazenar os dados de cada criptomoeda
all_data = []

# Função para processar os dados de cada criptomoeda
def download_and_process_data(symbol):
    try:
        # Baixa os dados históricos
        data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
        
        # Reseta o índice para garantir que a data seja uma coluna
        data.reset_index(inplace=True)
        
        # Renomeia as colunas para o formato desejado
        data.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
        
        # Adiciona a coluna 'Crypto' com o valor do símbolo
        data.insert(0, 'Crypto', symbol)
        
        # Adiciona os dados ao lista
        all_data.append(data)
        print(f"Data for {symbol} processed successfully.")
    except Exception as e:
        print(f"Error downloading data for {symbol}: {e}")

# Baixa e processa os dados para cada criptomoeda na lista
for symbol in symbols:
    download_and_process_data(symbol)

# Concatena todos os dados em um único DataFrame
combined_data = pd.concat(all_data, ignore_index=True)

# Salva os dados combinados em um único arquivo CSV
combined_data.to_csv(csv_path, index=False)
print(f"Combined data saved at: {csv_path}")
