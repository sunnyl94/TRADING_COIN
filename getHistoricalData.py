import ccxt
import pprint
import time
import pandas as pd

# 파일로부터 apiKey, Secret 읽기 
with open("Key/api.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip() 
    secret = lines[1].strip()

# binance 선물 객체 생성
binance_future = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

# binance 현물 객체 생성
# binance_spot = ccxt.binance(config={
#     'apiKey': api_key,
#     'secret': secret,
#     'enableRateLimit': True,
# })

# USDT의 잔고 조회 [현물]
# balance_spot = binance_spot.fetch_balance()
# # print(balance_spot['USDT'])

# USDT의 잔고 조회 [선물]
balance_future = binance_future.fetch_balance()
# print(balance_future['USDT'])

# since 날짜 변경
from_ts = binance_future.parse8601('2022-02-01 00:00:00')

btc = binance_future.fetch_ohlcv(
    symbol="BTC/USDT", 
    timeframe='5m', 
    since= from_ts)

# 선물 현재가
# btc_now =  binance_future.fetch_ticker("BTC/USDT")
# print(btc_now)

# 선물 과거 데이터
df = pd.DataFrame(btc, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])
df['Datetime'] = pd.to_datetime(df['Datetime'], unit='ms')
df.set_index('Datetime', inplace=True)


# df.to_csv(r'HistoricalData/binance_future_since_20220201.csv')







