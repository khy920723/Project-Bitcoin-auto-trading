# # ------------------------------------version 2.0-------------------------------------------
# now = datetime.datetime.now() # 현재시간
# start_time = get_start_time("KRW-BTC") # 업비트 BTC 시간 (09:00)
# end_time = start_time + datetime.timedelta(days=1)
# print(now)

# # 07:00-08:00 coin_flag 초기화
# if end_time - datetime.timedelta(seconds=7200) < now < end_time - datetime.timedelta(seconds=3600):
#     for i in coin_list:
#         coin_flag[i] = True

# # 매수 (08:30 < 현재 < 20:00)
# if end_time - datetime.timedelta(seconds=1800) < now < start_time - datetime.timedelta(seconds=39600):
#     krw = get_balance("KRW") # 원화 잔고 조회
#     devided_krw = krw/5 # 잔고의 1/5 투자
#     for i in coin_list:
#         print("********BUYING 08:30-20:00 {}**********".format(i))
#         k = best_k("KRW-{}".format(i), fee)
#         time.sleep(1) # 연산과 서버 연결 때문에 최소 1초 설정
#         target_price = get_target_price("KRW-{}".format(i), k) # 목표가
#         ma50 = get_ma50("KRW-{}".format(i)) # 3분봉 기준 MA 50
#         ma15 = get_ma15("KRW-{}".format(i)) # 3분봉 기준 MA 15
#         ma5 = get_ma5("KRW-{}".format(i)) # 3분봉 기준 MA 5
#         current_price = get_current_price("KRW-{}".format(i)) # 현재가
#         if target_price < current_price and ma5 < current_price: # 목표가<현재가 & MA15<현재가
#             if ma50 < ma15 and ma15 < ma5: # 15일 이평선 < 5일 이평선
#                 now_krw = get_balance("KRW")
#                 if devided_krw > 500000000 and now_krw > devided_krw:
#                     if coin_flag[i] == True: # 당일 매수 내역이 없다면 매수
#                         upbit.buy_market_order("KRW-{}".format(i), devided_krw * (1 - fee))
#                         coin_flag[i] = False
#                         print("{} buy ".format(i))
#         time.sleep(1) # 연산과 서버 연결 때문에 최소 1초 설정

# # 매도 (20:00 ~ +1 08:30)
# else:
#     for i in coin_list:
#         print("********SELLING {}**********".format(i))
#         ma15 = get_ma15("KRW-{}".format(i)) # 3분봉 기준 MA 15
#         ma5 = get_ma5("KRW-{}".format(i)) # 3분봉 기준 MA 5
#         if ma5 < ma15:
#             COIN = get_balance_sell(i)
#             AVG_BUY_PRICE = get_balance_sell2(i)
#             current_price = get_current_price("KRW-{}".format(i))
#             each = 5000 / current_price
#             if COIN != None and current_price > AVG_BUY_PRICE: # 코인이 존재하고 현재가가 매수평균가 보다 높을 시
#                 if COIN > each:
#                     upbit.sell_market_order("KRW-{}".format(i), COIN * (1 - fee))
#                     print("{} sell".format(i))
#         time.sleep(0.5)