# pip3 install python-binance

from binance import Client
import pandas as pd

# 파일로부터 apiKey, Secret 읽기 
with open("Key/api.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip() 
    api_secret = lines[1].strip()

client = Client(api_key, api_secret)

# Ignore 1000 row limit
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "1 Jan, 2022")

df = pd.DataFrame(klines, columns=["Datetime", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
df['Datetime'] = pd.to_datetime(df['Datetime'], utc=True, unit='ms')
df.set_index('Datetime', inplace=True)

df.to_csv(r'HistoricalData/binance_future_since_20220201_new.csv')

