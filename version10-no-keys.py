import requests
import pandas as pd
import time
import pyupbit
import datetime

# 업비트 API key
access = "Here is no key"
secret = "Here is no key"

# 로그인
upbit = pyupbit.Upbit(access, secret)


# 시작시간 조회
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


# KRW 잔고 조회 - 매수
def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                time.sleep(0.1)
                return float(b['balance'])
            else:
                time.sleep(0.1)
                return 0

# MACD 오실레이터
def get_macd_signal_now(ticker):
    macd_short, macd_long, macd_signal = 12, 26, 9 # 기본값
    df = pyupbit.get_ohlcv(ticker, interval='minute10', count=200)
    df["MACD_short"] = df['close'].ewm(span=macd_short).mean()
    df["MACD_long"] = df['close'].ewm(span=macd_long).mean()
    df["MACD"] = df.apply(lambda x: (x['MACD_short'] - x["MACD_long"]), axis=1)
    df["MACD_signal"] = df["MACD"].ewm(span=macd_signal).mean()
    macd_signal = df["MACD_signal"].iloc[-1]
    time.sleep(0.1)
    return macd_signal


# MACD 오실레이터
def get_macd_osc_now(ticker):
    macd_short, macd_long, macd_signal = 12, 26, 9 # 기본값
    df = pyupbit.get_ohlcv(ticker, interval='minute10', count=200)
    df["MACD_short"] = df['close'].ewm(span=macd_short).mean()
    df["MACD_long"] = df['close'].ewm(span=macd_long).mean()
    df["MACD"] = df.apply(lambda x: (x['MACD_short'] - x["MACD_long"]), axis=1)
    df["MACD_signal"] = df["MACD"].ewm(span=macd_signal).mean()
    df["MACD_oscillator"] = df.apply(lambda x: (x["MACD"] - x["MACD_signal"]), axis=1)
    macd_oscillator = df["MACD_oscillator"].iloc[-1]
    time.sleep(0.1)
    return macd_oscillator


# MACD 오실레이터
def get_macd_osc_before(ticker):
    macd_short, macd_long, macd_signal = 12, 26, 9 # 기본값
    df = pyupbit.get_ohlcv(ticker, interval='minute10', count=200)
    df["MACD_short"] = df['close'].ewm(span=macd_short).mean()
    df["MACD_long"] = df['close'].ewm(span=macd_long).mean()
    df["MACD"] = df.apply(lambda x: (x['MACD_short'] - x["MACD_long"]), axis=1)
    df["MACD_signal"] = df["MACD"].ewm(span=macd_signal).mean()
    df["MACD_oscillator"] = df.apply(lambda x: (x["MACD"] - x["MACD_signal"]), axis=1)
    macd_oscillator = df["MACD_oscillator"].iloc[-2]
    time.sleep(0.1)
    return macd_oscillator


def get_bolinserband_lbb(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='minute10')
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


def get_bolinserband_ubb(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='minute10')
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


# RSI 조회
def get_rsi(symbol):
    url = "https://api.upbit.com/v1/candles/minutes/10"
    querystring = {"market": symbol, "count": "500"}
    response = requests.request("GET", url, params=querystring)
    data = response.json()
    df = pd.DataFrame(data)
    df = df.reindex(index=df.index[::-1]).reset_index()
    df['close'] = df["trade_price"]
    def rsi(ohlc: pd.DataFrame, period: int = 14):
        ohlc["close"] = ohlc["close"]
        delta = ohlc["close"].diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        _gain = up.ewm(com=(period - 1), min_periods=period).mean()
        _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
        RS = _gain / _loss
        return pd.Series(100 - (100 / (1 + RS)), name="RSI")
    rsi = rsi(df, 14).iloc[-1]
    time.sleep(0.1)
    return rsi


# 현재가 조회
def get_current_price(ticker):
    time.sleep(0.1)
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


# ticker 잔고 조회 - 매도
def get_balance_sell_coin(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                time.sleep(0.1)
                return float(b['balance'])
            else:
                time.sleep(0.1)
                return 0


# KRW-BTC
krw_tickers = []
# BTC:0
krw_tickers_flag = []
krw_tickers_buy_count_flag = []
# 초기화 플래그
flag = False
# 수수료
fee = 0.0005
# 잔고의 1/N 투자 초기화 (초기화 else 부분 08:00-09:00 투자금 입력 / N = 투자종목개수 + 1 권장)
devided_krw = 0

# ------------------------------------version 6.0-------------------------------------------
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()  # 현재시간
        start_time = get_start_time("KRW-BTC")  # 업비트 BTC 시간 (09:00)
        end_time = start_time + datetime.timedelta(days=1)
        print("#####################" + str(now) + "#####################")

        # 09:00 - 09:00 + 1 요소들 이니셜라이즈
        if flag == False and start_time < now < end_time:
            url = "https://api.upbit.com/v1/market/all"
            resp = requests.get(url)
            data = resp.json()

            # krw_tickers
            for coin in data:
                ticker = coin['market']
                if ticker.startswith('KRW'):
                    krw_tickers.append(ticker)
            print(krw_tickers)
            time.sleep(0.1)

            # krw_tickers_flag
            for i in krw_tickers:
                krw_tickers_flag.append(0)
            print(krw_tickers_flag)
            time.sleep(0.1)

            for i in krw_tickers:
                krw_tickers_buy_count_flag.append(0)
            print(krw_tickers_buy_count_flag)
            time.sleep(0.1)

            # 투자금액 분배
            krw = get_balance("KRW")
            print(krw)
            time.sleep(0.1)
            devided_krw = krw / 2.1
            print(devided_krw)

            flag = True
            time.sleep(0.1)

        # 09:00 - 00:20 + 1 매수 및 매도
        elif flag == True and start_time + datetime.timedelta(seconds=39600) < now < end_time - datetime.timedelta(seconds=300):
            for ticker in krw_tickers:
                if krw_tickers_flag[krw_tickers.index(ticker)] == 0:
                    print("[매수] " + ticker)
                    rsi = get_rsi(ticker)
                    print("rsi: ", rsi)
                    if rsi < 20 and krw_tickers_buy_count_flag[krw_tickers.index(ticker)] < 2:
                        osc_now = get_macd_osc_now(ticker)
                        macd_signal = get_macd_signal_now(ticker)
                        print("osc_now: ", osc_now)
                        print("macd_signal: ", macd_signal)
                        if osc_now < 0 and macd_signal < 0:
                            lbb = get_bolinserband_lbb(ticker)
                            current = get_current_price(ticker)
                            print("lbb: ", lbb)
                            print("current: ", current)
                            if current < lbb and get_balance("KRW") > devided_krw > 5000:
                                upbit.buy_market_order(ticker, devided_krw * (1 - fee))
                                krw_tickers_flag[krw_tickers.index(ticker)] = 1
                                krw_tickers_buy_count_flag[krw_tickers.index(ticker)] += 1
                                print("! " + ticker + " buied ")
                                time.sleep(0.1)
                            time.sleep(0.1)
                        time.sleep(0.1)
                    time.sleep(0.1)

                else:
                    print("[매도] " + ticker)
                    # 코인 보유 & 5000원 어치가 넘을 때
                    if get_balance_sell_coin(ticker[4:]) != None and get_balance_sell_coin(ticker[4:]) > 5000 / get_current_price(ticker):
                        # 실제 매도 코드
                        # 익절 (13:00 전)
                        osc_now = get_macd_osc_now(ticker)
                        current = get_current_price(ticker)
                        rsi = get_rsi(ticker)
                        ubb = get_bolinserband_ubb(ticker)
                        if osc_now > 0 and rsi > 50:
                            upbit.sell_market_order(ticker, get_balance_sell_coin(ticker[4:]))
                            krw_tickers_flag[krw_tickers.index(ticker)] = 0
                            print("! " + ticker + " selled ")
                            time.sleep(0.1)
                        elif osc_now < 0 and rsi > 70:
                            upbit.sell_market_order(ticker, get_balance_sell_coin(ticker[4:]))
                            krw_tickers_flag[krw_tickers.index(ticker)] = 0
                            print("! " + ticker + " selled ")
                            time.sleep(0.1)
                        elif ubb < current:
                            upbit.sell_market_order(ticker, get_balance_sell_coin(ticker[4:]))
                            krw_tickers_flag[krw_tickers.index(ticker)] = 0
                            print("! " + ticker + " selled ")
                            time.sleep(0.1)
                        time.sleep(0.1)
                    time.sleep(0.1)
                time.sleep(0.1)
            # 전량매도
        else:
            for ticker in krw_tickers:
                print("[전량매도] " + ticker)
                if get_balance_sell_coin(ticker[4:]) != None and get_balance_sell_coin(ticker[4:]) > 5000 / get_current_price(ticker):
                    upbit.sell_market_order(ticker, get_balance_sell_coin(ticker[4:]))
                    print("! " + ticker + " selled ")
                    time.sleep(0.1)
                time.sleep(0.1)
            krw_tickers.clear()
            print(krw_tickers)
            krw_tickers_flag.clear()
            print(krw_tickers_flag)
            krw_tickers_buy_count_flag.clear()
            print(krw_tickers_buy_count_flag)
            flag = False
            time.sleep(0.1)
        time.sleep(0.1)

    # 예외처리
    except Exception as e:
        print(e)
        time.sleep(1)