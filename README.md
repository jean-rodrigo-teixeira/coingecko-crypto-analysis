# Projeto: Coleta de Dados de Criptomoedas

Este projeto tem como objetivo coletar dados sobre várias criptomoedas utilizando a API pública do [CoinGecko](https://www.coingecko.com/pt/api), armazenar as informações em um arquivo Excel e criar uma base para análises futuras. O script coleta dados de preços históricos das criptomoedas **Bitcoin**, **Ethereum**, **Ripple**, **Litecoin** e outras, dos últimos 365 dias, além de metadados sobre essas criptomoedas.

## Arquivos do Projeto

1. **`crypto_data.xlsx`**: Arquivo Excel gerado pelo script, contendo os seguintes dados:
   - **Aba `Coin_ID_and_Name`**: Contém o ID e o nome das criptomoedas coletadas.
   - **Aba `Coin_Metadata`**: Contém os metadados das criptomoedas, como preço atual (em USD), market cap, supply e max supply.
   - **Aba `Coin_Price_Data`**: Contém os preços históricos das criptomoedas, incluindo o timestamp e o preço (em USD) para cada dia dos últimos 365 dias.

2. **`extract_crypto_data.py`**: Script Python responsável por:
   - Fazer requisições à API do CoinGecko para coletar dados históricos de preços e metadados.
   - Processar os dados retornados (converter timestamps para datas legíveis).
   - Salvar os dados extraídos em um arquivo Excel (**`crypto_data.xlsx`**).

## Funcionalidades

- Coleta de dados históricos de preços das criptomoedas **Bitcoin**, **Ethereum**, **Ripple**, **Litecoin** e outras para os últimos 365 dias.
- Coleta de metadados das criptomoedas, como preço atual, market cap, supply e max supply.
- Conversão dos timestamps fornecidos pela API em datas legíveis.
- Salva os dados no formato Excel, com três abas: `Coin_ID_and_Name`, `Coin_Metadata`, e `Coin_Price_Data`.

## Como Usar

### Requisitos

Certifique-se de ter os seguintes pacotes instalados:

- `requests`
- `pandas`
- `openpyxl` (para salvar os dados no formato Excel)

Você pode instalar as dependências executando o seguinte comando:

```bash
pip install requests pandas openpyxl
