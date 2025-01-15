# Projeto de Extração e Análise de Dados de Criptomoedas

Este projeto tem como objetivo extrair dados históricos de preços de criptomoedas utilizando a API pública do [CoinGecko](https://www.coingecko.com/pt/api), salvá-los em um arquivo Excel e criar uma base para análises futuras.

## Arquivos do Projeto

1. **`crypto_data.xlsx`**: Arquivo Excel gerado pelo script, contendo os preços históricos das criptomoedas Bitcoin e Ethereum nos últimos 365 dias.  
   - Aba `Bitcoin`: Contém as colunas `Date` (data) e `Price` (preço em USD).
   - Aba `Ethereum`: Contém as colunas `Date` (data) e `Price` (preço em USD).

2. **`extract_crypto_data.py`**: Script Python responsável por:
   - Fazer requisições à API do CoinGecko.
   - Processar os dados retornados (converter timestamps para datas legíveis).
   - Salvar os dados extraídos em um arquivo Excel.

## Funcionalidades

- Extrai preços históricos de criptomoedas (Bitcoin e Ethereum) dos últimos 365 dias.
- Converte os timestamps fornecidos pela API em datas no formato legível.
- Salva os dados no formato Excel para facilitar análises futuras.

## Como Utilizar

### Pré-requisitos

1. **Python**: Certifique-se de ter o Python instalado (versão 3.7 ou superior).
2. **Bibliotecas Necessárias**:
   - `pandas`
   - `requests`
   
   Instale as dependências executando:
   ```bash
   pip install pandas requests
