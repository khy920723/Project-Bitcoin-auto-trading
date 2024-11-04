"""
업비트 이동평균값: ddengle.com/develop/5814674
pyupbit 함수: github.com/sharebook-kr/pyupbit
MA를 위한 rolling 함수: EnGeniUS의 55.이동하는 평균인 Moving average 게시글
"""


import pyupbit
import numpy as np
import time

# --------------------best k 값 구하는 코드----------------------
# k에 따른 ror 구하는 함수
def get_ror(ticker, k, interval, count):
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    print(df['target'])

    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror


# best k 구하는 함수
def best_k(ticker, interval, count):
    k_list = [] # 변동폭 리스트
    ror_list = [] # 수익률 리스트
    target_list = [] # 목표값 리스트 
    
    for k in np.arange(0.05, 1.0, 0.05):
        k_list.append(k)
        ror_list.append(get_ror(ticker, k, interval, count))
        time.sleep(0.06) # 0.05=JsonError , 0.06=Fine, 0.07=Fine 

    i = ror_list.index(max(ror_list))
    return k_list[i]

# 매수 목표가 (변동성 돌파 전략)
def get_target_price(ticker, k, interval, count):
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count) # 2일치 데이터 조회
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

while True:
    k_day = best_k("KRW-SXP", "day", 2)
    k_minute = best_k("KRW-SXP", "minute3", 20)
    k = (k_day + k_minute) / 2
    # k = k_minute
    target_price = get_target_price("KRW-SXP", k, interval="minute3", count=20)
    print("k = " + str(k) + ", target_price = " + str(target_price))
    time.sleep(0.05)
