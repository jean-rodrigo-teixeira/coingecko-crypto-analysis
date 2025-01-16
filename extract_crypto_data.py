import requests
import pandas as pd
import time  # Importando a função time.sleep
from datetime import datetime

# Função para pegar dados e metadados
def get_crypto_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    response = requests.get(url)
    
    # Verificando erro 429 e esperando 60 segundos
    if response.status_code == 429:
        print(f"Limite de requisições atingido para {coin_id}. Aguardando 60 segundos...")
        time.sleep(60)  # Aguardar 60 segundos
        response = requests.get(url)  # Repetir a requisição após o delay
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao acessar dados da moeda {coin_id}: Status Code {response.status_code}")
        return None

# Função para pegar dados históricos de preço
def get_historical_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {'vs_currency': 'usd', 'days': '365'}
    response = requests.get(url, params=params)
    
    # Verificando erro 429 e esperando 60 segundos
    if response.status_code == 429:
        print(f"Limite de requisições atingido para {coin_id}. Aguardando 60 segundos...")
        time.sleep(60)  # Aguardar 60 segundos
        response = requests.get(url, params=params)  # Repetir a requisição após o delay
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao acessar dados históricos para {coin_id}: Status Code {response.status_code}")
        return None

# Lista das moedas
coins = ['bitcoin', 'ethereum', 'ripple', 'litecoin']

# Criando listas para armazenar os dados
id_name_list = []
metadata_list = []
price_data_list = []

# Extraindo dados para cada moeda
for i, coin in enumerate(coins, start=1):
    print(f"Extraindo dados para {coin}...")
    try:
        # Obtendo os dados gerais da moeda
        data = get_crypto_data(coin)
        if data is None:
            continue
        
        # Obtendo os dados históricos de preço
        historical_data = get_historical_data(coin)
        if historical_data is None:
            continue
        
        # Verificando se os dados gerais estão disponíveis
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
        
        # Salvando os metadados
        metadata_list.append({
            'ID': i,
            'Coin': coin,
            'Current Price (USD)': current_price,
            'Market Cap (USD)': market_cap,
            'Total Supply': total_supply,
            'Max Supply': max_supply
        })
        
        # Salvando os dados históricos de preço
        if 'prices' in historical_data and historical_data['prices']:
            for price in historical_data['prices']:
                timestamp = price[0]  # Mantendo o timestamp original (em milissegundos)
                price_value = str(price[1]).replace(',', '.')  
                price_data_list.append({
                    'ID': i,
                    'Date': timestamp,  # Mantendo o timestamp original
                    'Price (USD)': price_value
                })
        else:
            print(f"Sem dados históricos para {coin} ou dados não disponíveis.")
        
        # Salvando a lista de ID e Nome para a Planilha 1
        id_name_list.append({
            'ID': i,
            'Coin': coin
        })

        print(f"Dados e metadados de {coin} salvos com sucesso.")
        
        # Adicionando uma pausa de 2 segundos entre as requisições
        time.sleep(2)  # Espera 2 segundos antes de prosseguir para a próxima moeda
        
    except KeyError as e:
        print(f"Erro ao acessar dados de {coin}: {e}")
    except Exception as e:
        print(f"Erro desconhecido ao acessar dados de {coin}: {e}")

# Convertendo as listas para DataFrames
id_name_df = pd.DataFrame(id_name_list)
metadata_df = pd.DataFrame(metadata_list)
price_data_df = pd.DataFrame(price_data_list)

# Salvando todos os dados em um arquivo Excel com 3 planilhas
with pd.ExcelWriter('crypto_data.xlsx') as writer:
    id_name_df.to_excel(writer, sheet_name='Coin_ID_and_Name', index=False)
    metadata_df.to_excel(writer, sheet_name='Coin_Metadata', index=False)
    price_data_df.to_excel(writer, sheet_name='Coin_Price_Data', index=False)

print("Todos os dados foram salvos com sucesso no arquivo 'crypto_data.xlsx'.")