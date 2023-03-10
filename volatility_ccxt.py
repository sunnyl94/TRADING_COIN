import ccxt
from pprint import pprint
import time
import pandas as pd
import datetime

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

leverage = 2

resp = binance_future.fapiPrivate_post_leverage({
    'symbol': 'BTCUSDT',
    'leverage': leverage
})

# 변동성 돌파 전략 target price 구하기
def get_target_price(binance_future):
    # 선물 과거 데이터
    btc = binance_future.fetch_ohlcv(
        symbol="BTC/USDT", 
        timeframe='1d',)
    
    # 불러온 과거 데이터 DataFrame 만들고 Datetime 변환
    df = pd.DataFrame(btc, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Datetime'] = pd.to_datetime(df['Datetime'], unit='ms')
    df.set_index('Datetime', inplace=True)

    volatility = (df.iloc[-2, 1] - df.iloc[-2, 2]) * 0.6    # (yesterday 종가 high - 종가 low) * k
    target_price = df.iloc[-1, 0] + volatility  # (today Open) + volatility
    return target_price

# 선물 매수 주문 및 롱 포지션 진입
def buy_crypto_currency(binance_future, current_price):
    # 현재 USDT 보유량
    balance_future = binance_future.fetch_balance()
    USDT_free = balance_future['USDT']["free"]
    unit = (USDT_free * 0.5) / current_price

    # market price로 진입
    order = binance_future.create_market_buy_order(
        symbol="BTC/USDT",
        amount=unit
    )
    print("==== Buy ORDER ====")
    pprint(order)

# 선물 매도 주문 및 롱 포지션 정리
def sell_crypto_current(binance_future):
    balance_future = binance_future.fetch_balance()
    BTC_position = balance_future['info']['positions']

    for position in BTC_position:
        if position["symbol"] == "BTCUSDT":
            pprint(position)
            positionAmt = position["positionAmt"]
    
    order = binance_future.create_market_sell_order(
        symbol="BTC/USDT",
        amount=positionAmt
    )

    print("==== Sell ORDER ====")
    pprint(order)

    

# current_btc =  binance_future.fetch_ticker("BTC/USDT")
# current_price = current_btc["close"]
# buy_crypto_currency(binance_future, current_price)
sell_crypto_current(binance_future)


    
target_price = get_target_price(binance_future)

# 매수용 Flag
hold_flag = False

while True:
    # 선물 현재가
    current_btc =  binance_future.fetch_ticker("BTC/USDT")
    current_price = current_btc["close"]

    buy_crypto_currency(binance_future, current_price)

    # 현재 시간
    timestamp = current_btc["timestamp"] / 1000
    now = datetime.datetime.fromtimestamp(timestamp)

    print("Target Price: ", target_price)

    if target_price <= current_price and hold_flag == False:
        print("==== BUY!! ====")
        # buy_crypto_currency()

    time.sleep(1)

    print(now, ": ", current_price)

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
# balance_future = binance_future.fetch_balance()
# print(balance_future['USDT'])


# print(btc_now)








