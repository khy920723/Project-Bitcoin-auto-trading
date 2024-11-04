"""
업비트 이동평균값: ddengle.com/develop/5814674
pyupbit 함수: github.com/sharebook-kr/pyupbit
MA를 위한 rolling 함수: EnGeniUS의 55.이동하는 평균인 Moving average 게시글
"""

import time
import pyupbit
import datetime
import numpy as np


# ticker: 코인종류
# k: 변동폭

# best_k 구하기 위한 수익률 함수
def get_ror(ticker, k, fee, interval, count):
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    fee = fee
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)
    ror = df['ror'].cumprod()[-2]
    return ror


# best k 구하는 함수
def best_k(ticker, fee, interval, count):
    k_list = []  # 변동폭 리스트
    ror_list = []  # 수익률 리스트
    for k in np.arange(0.01, 1.0, 0.01):
        k_list.append(k)
        ror_list.append(get_ror(ticker, k, fee, interval, count))
        time.sleep(0.08)  # 0.05=JsonError , 0.07=JsonError
    i = ror_list.index(max(ror_list))
    return k_list[i]


# 매수 목표가 (변동성 돌파 전략)
def get_target_price(ticker, k, interval, count):
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)  # 2일치 데이터 조회
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


# 시작시간 조회
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


# 3분봉 기준 50 이동평균선(MA 50) 조회
def get_ma50(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='minute3', count=50)
    ma50 = df['close'].rolling(50).mean().iloc[-1]
    return ma50


# 3분봉 기준 30 이동평균선(MA 30) 조회
def get_ma30(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='minute3', count=30)
    ma30 = df['close'].rolling(30).mean().iloc[-1]
    return ma30


# 3분봉 기준 15개 이동평균선(MA 15) 조회
def get_ma15(ticker):
    """3분봉 기준 15일 이동 평균선(MA 15) 조회"""
    df = pyupbit.get_ohlcv(ticker, interval='minute3', count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15


# 3분봉 기준 5개 이동평균선(MA 5) 조회
def get_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='minute3', count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5


# KRW 잔고 조회 - 매수
def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0


# ticker 잔고 조회 - 매도
def get_balance_sell_coin(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0


# ticker 매수평균가 조회 - 매도
def get_balance_sell_avg_buy_price(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0


# 현재가 조회
def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


# 업비트 API key
access = "Here is your key"
secret = "Here is your key"

# 로그인
upbit = pyupbit.Upbit(access, secret)

fee = 0.0005  # 수수료

# 코인 리스트 (코인 추가 시 해당 코드 변경 / 4개 종목 권장 / 종목이 많을 수록 슬리피지가 높아짐)
coin_list = ["BTC", "SXP", "ARK", "DOGE"]

# 매수 플래그 (True -> 매수 / 코인 추가 시 해당 코드 2차 변경)
coin_flag = {"BTC": True, "SXP": True, "ARK": True, "DOGE": True}

# 매수 회수 (투자 회수 늘리고 싶을 시 매수코드에서 해당 범위값 변경)
coin_buy_count = {"BTC": 0, "EOS": 0, "BCH": 0, "XEM": 0, "SXP": 1, "LTC": 0, "JST": 0, "XTZ": 0, "BTT": 0, "DOGE": 1,
                  "ARK": 0}

# best k의 day기준 2일 딕셔너리 (08:00 초기화, 09:00 업데이트 이후 고정값)
coin_k_day = {"BTC": None, "EOS": None, "BCH": None, "XEM": None, "SXP": None, "LTC": None, "JST": None, "XTZ": None,
              "BTT": None, "DOGE": None, "ARK": None}

# 손실율 패널티 딕셔너리
coin_loss_score = {"BTC": 0, "EOS": 0, "BCH": 0, "XEM": 0, "SXP": 0, "LTC": 0, "JST": 0, "XTZ": 0, "BTT": 0,
                   "DOGE": 0, "ARK": 0}

# 잔고의 1/N 투자 초기화 (초기화 else 부분 08:00-09:00 투자금 입력 / N = 투자종목개수 + 1 권장)
devided_krw = 10000

# ------------------------------------version 3.0-------------------------------------------
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()  # 현재시간
        start_time = get_start_time("KRW-BTC")  # 업비트 BTC 시간 (09:00)
        end_time = start_time + datetime.timedelta(days=1)
        print("#####################" + str(now) + "#####################")

        if start_time < now < end_time - datetime.timedelta(seconds=600):
            for i in coin_list:
                # 매수 (09:00 < 현재 < 08:00 +1)
                if coin_flag[i] == True:
                    print("**************************try buying {}***************************".format(i))
                    now_krw = get_balance("KRW")  # 원화 잔고 조회
                    print("now krw = " + str(now_krw))
                    print("divided krw = " + str(devided_krw))
                    if coin_k_day[i] == None:
                        time.sleep(0.08)  # 연산과 서버 연결 때문에 최소 1초 설정
                        coin_k_day[i] = best_k("KRW-{}".format(i), fee, "day", 2)  # 얘는 09:00부터 고정
                        print("! {} coin_k_day updated".format(i))
                        k_minute = best_k("KRW-{}".format(i), fee, "minute3", 30)
                        k = (coin_k_day[i] + k_minute) / 2
                        target_price = get_target_price("KRW-{}".format(i), k, interval="minute3", count=90)  # 목표가
                        ma30 = get_ma30("KRW-{}".format(i))  # 3분봉 기준 MA 50
                        ma15 = get_ma15("KRW-{}".format(i))  # 3분봉 기준 MA 15
                        ma5 = get_ma5("KRW-{}".format(i))  # 3분봉 기준 MA 5
                        current_price = get_current_price("KRW-{}".format(i))  # 현재가
                        print("best k = " + str(k))
                        print("target price = ", str(target_price))
                        print("current price = " + str(current_price))
                        print("MA 30 = " + str(ma30))
                        print("MA 15 = " + str(ma15))
                        print("MA 5 = " + str(ma5))
                        print("flag = " + str(coin_flag[i]))
                        print("buy count = " + str(coin_buy_count[i]))
                        print("loss score = " + str(coin_loss_score[i]))
                        if now_krw > devided_krw:
                            if target_price < current_price:  # 목표가 < 현재가
                                if ma5 < current_price:
                                    if ma15 < ma5:
                                        if ma30 < ma5:
                                            print("! {} buying available".format(i))
                                            if devided_krw > 5000:
                                                if coin_buy_count[i] < 10:  # 종목 1개 당 카운트 4
                                                    if coin_loss_score[i] < 5:  # loss 패널티 한도
                                                        upbit.buy_market_order("KRW-{}".format(i),
                                                                               devided_krw * (1 - fee))
                                                        coin_flag[i] = False
                                                        coin_buy_count[i] += 1
                                                        print("! {} buied ".format(i))
                                                        print("coin buy count = " + str(coin_buy_count[i]))
                                                        print("coin loss score = " + str(coin_loss_score[i]))
                                                    else:
                                                        print("! coin loss score over")
                                                else:
                                                    print("! coin buy count over")
                                            else:
                                                print("! divided_krw is under 5000")
                        else:
                            print("! now krw lack")
                    else:
                        time.sleep(0.08)  # 연산과 서버 연결 때문에 최소 1초 설정
                        k_minute = best_k("KRW-{}".format(i), fee, "minute3", 30)
                        k = (coin_k_day[i] + k_minute) / 2
                        target_price = get_target_price("KRW-{}".format(i), k, interval="minute3", count=90)  # 목표가
                        ma30 = get_ma30("KRW-{}".format(i))  # 3분봉 기준 MA 50
                        ma15 = get_ma15("KRW-{}".format(i))  # 3분봉 기준 MA 15
                        ma5 = get_ma5("KRW-{}".format(i))  # 3분봉 기준 MA 5
                        current_price = get_current_price("KRW-{}".format(i))  # 현재가
                        print("best k = " + str(k))
                        print("target price = ", str(target_price))
                        print("current price = " + str(current_price))
                        print("MA 30 = " + str(ma30))
                        print("MA 15 = " + str(ma15))
                        print("MA 5 = " + str(ma5))
                        print("flag = " + str(coin_flag[i]))
                        print("buy count = " + str(coin_buy_count[i]))
                        print("loss score = " + str(coin_loss_score[i]))
                        if now_krw > devided_krw:
                            if target_price < current_price:  # 목표가 < 현재가
                                if ma5 < current_price:
                                    if ma15 < ma5:
                                        if ma30 < ma15:
                                            print("! {} buying available".format(i))
                                            if devided_krw > 5000:
                                                if coin_buy_count[i] < 10:  # 종목 1개 당 카운트 4
                                                    if coin_loss_score[i] < 5:  # loss 패널티 한도
                                                        upbit.buy_market_order("KRW-{}".format(i),
                                                                               devided_krw * (1 - fee))
                                                        coin_flag[i] = False
                                                        coin_buy_count[i] += 1
                                                        print("! {} buied ".format(i))
                                                        print("coin buy count = " + str(coin_buy_count[i]))
                                                        print("coin loss score = " + str(coin_loss_score[i]))
                                                    else:
                                                        print("! coin loss score over")
                                                else:
                                                    print("! coin buy count over")
                                            else:
                                                print("! divided_krw is under 5000")
                        else:
                            print("! now krw lack")

                # 매도 (09:00 < 현재 < 08:00 +1)
                else:
                    print("-------------------------try selling {}---------------------------".format(i))
                    time.sleep(0.08)  # 연산과 서버 연결 때문에 최소 1초 설정
                    ma30 = get_ma30("KRW-{}".format(i))  # 3분봉 기준 MA 30
                    ma15 = get_ma15("KRW-{}".format(i))  # 3분봉 기준 MA 15
                    ma5 = get_ma5("KRW-{}".format(i))  # 3분봉 기준 MA 5
                    time.sleep(0.08)  # 연산과 서버 연결 때문에 최소 1초 설정
                    COIN = get_balance_sell_coin(i)  # 해당 코인 보유 개수 조회
                    AVG_BUY_PRICE = get_balance_sell_avg_buy_price(i)  # 해당 코인 매수평균가 조회
                    current_price = get_current_price("KRW-{}".format(i))
                    each = 5000 / current_price
                    print("avg buy price = " + str(AVG_BUY_PRICE))
                    print("current price = " + str(current_price))
                    print("ma30 = " + str(ma30))
                    print("ma15 = " + str(ma15))
                    print("ma5 = " + str(ma5))
                    print("flag = " + str(coin_flag[i]))
                    print("buy count = " + str(coin_buy_count[i]))
                    print("loss score = " + str(coin_loss_score[i]))
                    if COIN != None:
                        if COIN > each:  # 코인이 5천원 어치가 있는 지 확인
                            if ma5 <= ma30:  # ma5가 ma30 보다 작을 때 무조건 매도
                                upbit.sell_market_order("KRW-{}".format(i), COIN)
                                print("! {} selled".format(i))
                                coin_flag[i] = True
                                if current_price < AVG_BUY_PRICE:
                                    coin_loss_score[i] = coin_loss_score[i] + (
                                                (AVG_BUY_PRICE / current_price - 1) * 100)
                                    print("loss score = " + str(coin_loss_score[i]))
                            if ma5 * 1.003 <= ma15:  # ma5가 ma15 보다 1.005배 적을 때 무조건 매도 (버티기)
                                upbit.sell_market_order("KRW-{}".format(i), COIN)
                                print("! {} selled".format(i))
                                coin_flag[i] = True
                                if current_price < AVG_BUY_PRICE:
                                    coin_loss_score[i] = coin_loss_score[i] + (
                                                (AVG_BUY_PRICE / current_price - 1) * 100)
                                    print("loss score = " + str(coin_loss_score[i]))
                            if current_price >= AVG_BUY_PRICE * 1.4:  # 수익률 40%일 때 무조건 매도 (익절)
                                upbit.sell_market_order("KRW-{}".format(i), COIN)
                                print("! {} selled".format(i))
                                coin_flag[i] = False
                                if current_price < AVG_BUY_PRICE:  # 익절이라 loss score 필요 없음
                                    coin_loss_score[i] = coin_loss_score[i] + (
                                                (AVG_BUY_PRICE / current_price - 1) * 100)
                                    print("loss score = " + str(coin_loss_score[i]))
                            if current_price <= AVG_BUY_PRICE * 0.95:  # 평균매수가 보다 -5%일 때 무조건 매도 (손절)
                                upbit.sell_market_order("KRW-{}".format(i), COIN)
                                print("! {} selled".format(i))
                                coin_flag[i] = True
                                if current_price < AVG_BUY_PRICE:
                                    coin_loss_score[i] = coin_loss_score[i] + (
                                                (AVG_BUY_PRICE / current_price - 1) * 100)
                                    print("loss score = " + str(coin_loss_score[i]))
                        else:
                            print("! coin already selled (COIN > each)")
                time.sleep(0.08)  # 연산과 서버 연결 때문에 최소 1초 설정

        # 전량 매도 및 플래그 초기화 (08:00 +1 - 09:00 +1)
        else:
            for i in coin_list:
                time.sleep(0.08)  # 연산과 서버 연결 때문에 최소 1초 설정
                COIN = get_balance_sell_coin(i)  # 해당 코인 보유 개수 조회
                current_price = get_current_price("KRW-{}".format(i))
                each = 5000 / current_price
                if COIN != None:
                    if COIN > each:
                        upbit.sell_market_order("KRW-{}".format(i), COIN)
                        print("{} selled".format(i))
                coin_flag[i] = True
                print("! {} ".format(i) + "coin flag initialized")
                print("flag = " + str(coin_flag[i]))
                coin_buy_count[i] = 0
                print("! {} ".format(i) + "buy count initialized")
                print("buy count = " + str(coin_buy_count[i]))
                coin_loss_score[i] = 0
                print("! {} ".format(i) + "coin loss score initialized")
                print("loss score = " + str(coin_loss_score[i]))
                time.sleep(0.08)  # 연산과 서버 연결 때문에 최소 1초 설정s
                coin_k_day[i] = None
                print("! {} ".format(i) + "coin k day initialized")
                print("coin k day = " + str(coin_k_day[i]))
                krw = get_balance("KRW")  # 원화 잔고 조회
                devided_krw = krw / 3
                print("! divided_krw initialized")
                print("divided krw = " + str(devided_krw))
                time.sleep(0.08)  # 연산과 서버 연결 때문에 최소 1초 설정
            time.sleep(0.08)  # 연산과 서버 연결 때문에 최소 1초 설정

    # 예외처리
    except Exception as e:
        print(e)
        time.sleep(1)