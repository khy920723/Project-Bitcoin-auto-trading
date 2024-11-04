import pyupbit
import random
import numpy as np
import time
import datetime
import requests

# access = "Here is your key"          # 본인 값으로 변경
# secret = "Here is your key"          # 본인 값으로 변경
# upbit = pyupbit.Upbit(access, secret)
#
# print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
# print(upbit.get_balance("KRW"))         # 보유 현금 조회
#
#
# coin_list = ["DOGE", "WAXP", "MED", "VET", "BTT", "NEO", "QTUM", "GAS", "DAWN", "SC", "META", "SXP", "CHZ", "WAVES",
#              "GRS", "TRX", "BORA", "RFR", "TT", "CRO", "ELF", "LBC", "OMG", "EMC2", "STX", "ZRX", "ETC", "FLOW",
#              "LTC", "SRM", "SAND", "STPT", "STRAX", "MFT", "BCHA", "LINK", "ATOM"]
#
# coin_list_shuffled = []
# random.shuffle(coin_list)
# coin_list_shuffled = coin_list
# print(coin_list_shuffled)
# 3분봉 기준 5개 이동평균선(MA 5) 조회
def get_bolinserband_ubb(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='minute30')
    w = 20  # 기준 이동평균일
    k = 2  # 기준 상수
    # 중심선 (MBB) : n일 이동평균선
    df["mbb"] = df["close"].rolling(w).mean()
    df["MA20_std"] = df['close'].rolling(w).std()
    # 상한선 (UBB) : 중심선 + (표준편차 × K)
    # 하한선 (LBB) : 중심선 - (표준편차 × K)
    df["ubb"] = df.apply(lambda x: x["mbb"] + k * x["MA20_std"], 1)
    time.sleep(0.1)
    return df["ubb"].iloc[-1]

# 3분봉 기준 5개 이동평균선(MA 5) 조회
def get_bolinserband_lbb(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='minute30')
    w = 20  # 기준 이동평균일
    k = 2  # 기준 상수
    # 중심선 (MBB) : n일 이동평균선
    df["mbb"] = df["close"].rolling(w).mean()
    df["MA20_std"] = df['close'].rolling(w).std()
    # 상한선 (UBB) : 중심선 + (표준편차 × K)
    # 하한선 (LBB) : 중심선 - (표준편차 × K)
    df["lbb"] = df.apply(lambda x: x["mbb"] - k * x["MA20_std"], 1)
    time.sleep(0.1)
    return df["lbb"].iloc[-1]

# i = [0]
# print(i)
#
# now = datetime.datetime.now()  # 현재시간
# print(now)
# i[0] = now
# print(i)

# KRW-BTC
krw_tickers = []

url = "https://api.upbit.com/v1/market/all"
resp = requests.get(url)
data = resp.json()

for coin in data:
    ticker = coin['market']
    if ticker.startswith('KRW'):
        krw_tickers.append(ticker)
print(krw_tickers)

while True:
    for ticker in krw_tickers:
        print(ticker, get_bolinserband_lbb(ticker), get_bolinserband_ubb(ticker))
    time.sleep(0.5)
