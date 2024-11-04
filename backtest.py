import pyupbit
import numpy as np

# OHLCV 7일 동안의 값을 불러오는 코드
df = pyupbit.get_ohlcv("KRW-IGNIS", count=2)

# 변동성 돌파 전략에서 매수가를 구하기 위한 코드
# 변동폭 * k 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * 0.05

# target(매수가)
# range는 전날이기 때문에 컬럼을 한 칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

# ror(수익률)
# np.where(조건문, 참일 때 값, 거짓일 때 값)
# fee = 0.05
df['ror'] = np.where(df['high'] > df['target'], # 매수가 진행이 된 상황(목표가 보다 고가가 높을 경우)
                     df['close'] / df['target'], # 종가/목표가 (수익률)
                     1) # 아닐 경우 매수가 이뤄지지 않기 때문에 1

# 누적 곱 계산(cumprod) => 누적수익률
df['hpr'] = df['ror'].cumprod()

# 하락폭(Draw Down) 계산
# 누적 최대값과 현재 hpr 차이 / 누적 최대값 * 100
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# Max Draw Down (최대 하락폭)
print("MDD(%): ", df['dd'].max())

# 엑셀 출력
df.to_excel("dd.xlsx")

