        # # ------------------------------------version 1.0-------------------------------------------
        # now = datetime.datetime.now()
        # start_time = get_start_time("KRW-DOGE")
        # end_time = start_time + datetime.timedelta(days=1)
        # print("DOGE start, KRW: " + str(get_balance("KRW")) + ", DOGE: " + str(get_balance("DOGE")))

        # if start_time < now < end_time - datetime.timedelta(seconds=25200):
        #     target_price = get_target_price("KRW-DOGE", edit_k)
        #     # ma15 = get_ma15("KRW-DOGE")
        #     current_price = get_current_price("KRW-DOGE")
        #     if target_price < current_price:
        #         krw = get_balance("KRW")
        #         devided_krw = krw/5
        #         if devided_krw > 5000:
        #             if DOGE_flag == True:
        #                 upbit.buy_market_order("KRW-DOGE", devided_krw*(1-edit_fee))
        #                 DOGE_flag = False
        #                 print("DOGE buy, KRW: " + str(get_balance("KRW")) + ", DOGE: " + str(get_balance("DOGE")))
        # else:
        #     DOGE = get_balance("DOGE")
        #     current_price = get_current_price("KRW-DOGE")
        #     each = 5000 / current_price
        #     if DOGE != None:
        #         if DOGE > each:
        #             upbit.sell_market_order("KRW-DOGE", DOGE*(1 - edit_fee))
        #             DOGE_flag = True
        #             print("DOGE sell, KRW: " + str(get_balance("KRW")) + ", DOGE: " + str(get_balance("DOGE")))
        # time.sleep(1)

    # except Exception as e:
    #     print(e)
    #     time.sleep(1)

