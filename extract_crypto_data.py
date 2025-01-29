import yfinance as yf
import os

# Define o símbolo do Bitcoin no Yahoo Finance
symbol = "BTC-USD"

# Define o período de tempo desejado
start_date = "2010-01-01"  # Data inicial
end_date = "2025-01-01"    # Data final

# Obtém o caminho da variável de ambiente CRYPTO_DATA_PATH
crypto_data_path = os.getenv("CRYPTO_DATA_PATH")

# Se a variável não estiver definida, lança um erro
if not crypto_data_path:
    raise EnvironmentError("A variável de ambiente 'CRYPTO_DATA_PATH' não está definida.")

# Verifica se o caminho existe; se não, cria a pasta
if not os.path.exists(crypto_data_path):
    os.makedirs(crypto_data_path)

# Define o caminho completo para salvar o arquivo
csv_path = os.path.join(crypto_data_path, "crypto_price_data.csv")

# Baixa os dados históricos
try:
    data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
    
    # Salva os dados como CSV
    data.to_csv(csv_path)
    print(f"Dados salvos em: {csv_path}")
except Exception as e:
    print(f"Erro ao baixar os dados: {e}")
