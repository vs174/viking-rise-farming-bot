import dateutil
import time
import datetime as dt
# import win32com.client
import xlwings as xw
# import openpyxl
# from pandas.io import excel

import FinanceDataReader as fdr
from audioplayer import AudioPlayer
from navertts import NaverTTS
from module import upbit as ubt, upbit
from threading import Thread
import requests
import logging
import pyupbit
from decimal import Decimal
import pandas as pd
import numpy
import sys

from multiprocessing import Process

def play_volume(text):
    tts = NaverTTS(text)
    tts.save('alert_volume.mp3')
    AudioPlayer('alert_volume.mp3').play(block=True)


def play_price(text):
    tts = NaverTTS(text)
    tts.save('alert_price.mp3')
    AudioPlayer('alert_price.mp3').play(block=True)


def play_rsi(text):
    tts = NaverTTS(text)
    tts.save('alert_rsi.mp3')
    AudioPlayer('alert_rsi.mp3').play(block=True)


def play_sell(text):
    tts = NaverTTS(text)
    tts.save('alert_sell.mp3')
    AudioPlayer('alert_sell.mp3').play(block=True)


def play_oveall_amt(text):
    tts = NaverTTS(text)
    tts.save('alert_amt.mp3')
    AudioPlayer('alert_amt.mp3').play(block=True)


def play_5up(text):
    tts = NaverTTS(text)
    tts.save('alert_5up.mp3')
    AudioPlayer('alert_5up.mp3').play(block=True)


def play_5down(text):
    tts = NaverTTS(text)
    tts.save('alert_5down.mp3')
    AudioPlayer('alert_5down.mp3').play(block=True)


def play(text):
    tts = NaverTTS(text)
    tts.save('alert.mp3')
    AudioPlayer('alert.mp3').play(block=True)


# -----------------------------------------------------------------------------
# - Name : start_selltrade
# - Desc : 매도 로직
# - Input
# 1) sell_pcnt : 매도 수익률
# 2) dcnt_pcnt : 고점대비 하락률
# -----------------------------------------------------------------------------
def sell_called():  # (sell_pcnt, dcnt_pcnt):
    try:
        # access_key = "lYhlqKFhiIHfY1mVD0X0aorrn5ZCxVUzixImek8Q"  # 의
        # secret_key = "Sa6uchbtfiD4DnM5vJ9ze4ECWtMZZMPb7YH6AnMv"  # 호
        #
        # upbit = Upbit(access_key, secret_key)
        #
        print('5 sell_called ')
        upbit.set_loglevel("I")
        최소익절율 = 0.382        # 0.236 익절하려면 적어도 2.0%는 먹어야 한다.
        익절고점하락율 = -0.236    # 0.382 익절기회에서 고점대비 하락율이 -1% 이상 떨어지면 강제익절한다.
        손절율 = -0.886          # 0.236               # -0.382 -0.618        # 1.61 / 4.0 # 1.61        # 손절하려면 적어도 -1.5% 밑으로 떨어지면 바로 손절한다.
        save_수익율 = ''
        save_수익율2 = ''

        wb = xw.Book.caller()
        sh2 = wb.sheets('4H')  # Worksheet 설정

        # ----------------------------------------------------------------------
        # 반복 수행
        # ----------------------------------------------------------------------
        # while True:
        # ------------------------------------------------------------------
        # 보유 종목조회
        # ------------------------------------------------------------------
        target_items = upbit.get_accounts('Y', 'KRW')
        # ------------------------------------------------------------------
        # 보유 종목 현재가 조회
        # ------------------------------------------------------------------

        target_items_comma = upbit.chg_account_to_comma(target_items)

        tickers = upbit.get_ticker(target_items_comma)
        # -----------------------------------------------------------------
        # 보유 종목별 진행
        # -----------------------------------------------------------------



        for target_item in target_items:
            # print(target_item['korean_name'])
            for ticker in tickers:
                time.sleep(0.2)
                if target_item['market'] == ticker['market'] :
                    time.sleep(0.2)
                    # print('.', end='X')
                    # -------------------------------------------------
                    # 고점을 계산하기 위해 최근 매수일시 조회
                    # 1. 해당 종목에 대한 거래 조회(done, cancel)
                    # 2. 거래일시를 최근순으로 정렬
                    # 3. 매수 거래만 필터링
                    # 4. 가장 최근 거래일자부터 현재까지 고점을 조회
                    # -------------------------------------------------
                    order_done = upbit.get_order_status(target_item['market'], 'done') + upbit.get_order_status(
                        target_item['market'], 'cancel')
                    order_done_sorted = upbit.orderby_dict(order_done, 'created_at', True)
                    order_done_filtered = upbit.filter_dict(order_done_sorted, 'side', 'bid')
                    # -------------------------------------------------
                    # 매수 직후 나타나는 오류 체크용 마지막 매수 시간 차이 계산
                    # -------------------------------------------------
                    # 마지막 매수 시간
                    # 마지막 매수 시간
                    last_buy_dt = dt.datetime.strptime(
                        dateutil.parser.parse(order_done_filtered[0]['created_at']).strftime('%Y-%m-%d %H:%M:%S'),
                        '%Y-%m-%d %H:%M:%S')

                    # 현재 시간 추출
                    current_dt = dt.datetime.strptime(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                   '%Y-%m-%d %H:%M:%S')

                    # 시간 차이 추출
                    diff = current_dt - last_buy_dt

                    # 매수 후 1분간은 진행하지 않음(업비트 오류 방지 용)
                    if diff.seconds < 60:  # 60
                        logging.info('- 매수 직후 발생하는 오류를 방지하기 위해 진행하지 않음!!!' + str(diff.seconds))
                        logging.info('------------------------------------------------------')
                        continue

                    days = 1  # 최근 n일의 데이터 수집
                    idx = "UBMI"  # 인덱스명
                    # idx = "UBAI"  # 인덱스명
                    step = "1"
                    ## url = "https://crix-api-cdn.upbit.com/v1/crix/candles/minutes/" + step + "?code=IDX.UPBIT." + idx + "&count=" + str(days)
                    ## data = requests.get(url).json()
                    # print(최소익절율)
                    # sell_pcnt = 최소익절율 + 최소익절율

                    # sell_pcnt = 최소익절율 + (float(최소익절율) * float(data[0]['tradePrice'] - float(data[0]['openingPrice'])) / float(data[0]['openingPrice']) * 100.0 * 100.0) / 100.0 * 3.0
                    # dcnt_pcnt = 익절고점하락율 + (float(익절고점하락율) * float(data[0]['tradePrice'] - float(data[0]['openingPrice'])) / float(data[0]['openingPrice']) * 100.0 * 100.0) / 100.0 * 3.0
                    # sell_pcnt = round(sell_pcnt, 2)
                    # dcnt_pcnt = round(dcnt_pcnt, 2)

                    # print(sell_pcnt)
                    # print(dcnt_pcnt)
            # -----------------------------------------------------
                    # 수익률 계산
                    # ((현재가 - 평균매수가) / 평균매수가) * 100
                    # -----------------------------------------------------
                    수익율 = round(((Decimal(str(ticker['trade_price'])) - Decimal(
                        str(target_item['avg_buy_price']))) / Decimal(str(target_item['avg_buy_price']))) * 100, 2)
                    # print(수익율)

                    # sell_pcnt = Decimal(최소익절율) + (Decimal(최소익절율) * 수익율) / Decimal(10.0)
                    # dcnt_pcnt = Decimal(익절고점하락율) - (Decimal(익절고점하락율) * 수익율) / Decimal(10.0)

                    # if save_수익율 != str(수익율):
                    #     logging.info('종목:' + str(target_item['market']) + ' 평균매수가:' + str(target_item['avg_buy_price']) + ' 현재가:' + str(ticker['trade_price']) + ' [수익률:' + str(수익율) +'%]')

                    # -----------------------------------------------------
                    # 현재 수익률이 매도 수익률 이상인 경우에만 진행
                    # -----------------------------------------------------
                    #                      수익의 -5배일때 눈물을 머금고. 매도.
                    # k = -0.2 # -0.4  # 기냥 팔아버려야 하는 수익률 : 1.5 * -2.5 = -3.75, 1.5* -0.4 = -0.6
                    # print(0, '목표판매가(살짝변동) :', str(Decimal(str(sell_pcnt * (k)))) , '수익율 :' ,str(수익율))
                    # sell_pcnt = 최소익절율  # 익절율
                    # dcnt_pcnt = 익절고점하락율  # 고점대비하락율

                    # -0.25  <                   0.5                     and              0.5        <            1.0   수익율
                    # if (Decimal(str(손절율)) < Decimal(str(수익율))) and (Decimal(str(수익율)) < Decimal(str(sell_pcnt))):
                    #     if save_수익율 != str(수익율):
                    #         # logging.info('- 현재 수익률이 매도 수익률 보다 낮아 진행하지 않음!!!')
                    #         print('                                                    ',str(target_item['market']), ' 1/3. 수익율은 {0:>5}'.format(Decimal(str(수익율))),
                    #               '% 이며', Decimal(str(sell_pcnt)), '보다 높거나', str(손절율),
                    #               '보다 낮으면 매도 시도')
                    #     save_수익율 = str(수익율)
                    #     continue  # 다시 위로 올라 간다.
                    #
                    # save_수익율 = str(수익율)

                    # ------------------------------------------------------------------
                    # 캔들 조회
                    # ------------------------------------------------------------------
                    candles = upbit.get_candle(target_item['market'], '1', 200)  # 60  200

                    # ------------------------------------------------------------------
                    # 최근 매수일자 다음날부터 현재까지의 최고가를 계산
                    # ------------------------------------------------------------------
                    df = pd.DataFrame(candles)
                    mask = df['candle_date_time_kst'] > order_done_filtered[0]['created_at']
                    filtered_df = df.loc[mask]
                    highest_high_price = numpy.max(filtered_df['high_price'])
                    # print(highest_high_price)
                    # -----------------------------------------------------
                    # 고점대비 하락률
                    # ((현재가 - 최고가) / 최고가) * 100
                    # -----------------------------------------------------
                    현재고점대비하락율 = round(((Decimal(str(ticker['trade_price'])) - Decimal(
                        str(highest_high_price))) / Decimal(str(highest_high_price))) * 100, 2)
                    if save_수익율2 != str(수익율):
                        st = str(target_item['market']) + ' 수익율 [' + str(수익율) + '] ' + '' + '고점대비하락률 [' + str(
                        현재고점대비하락율) + '] <= ' + str(손절율) + ' 고점대비설정하락율 매수후 최고단가/평가손익/평가금액 ' + str(
                        highest_high_price) + ' [' + str(round(float(target_item['balance']) * (
                                float(ticker['trade_price']) - float(target_item['avg_buy_price'])),
                                                               0)) + '] ' + str(
                        round(float(target_item['balance']) * float(ticker['trade_price']), 0))
                        sh2['U' + str(int(19))].value = st
                        time.sleep(0.2)
                        logging.info(st)

                        # wb = xw.Book.caller()
                        # sh2 = wb.sheets('4H')  # Worksheet 설정
                        myt = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        r = sh2['c5'].value

                        # sh2['R' + str(int(r+2))].value = sh2['R' + str(int(r+1))].value
                        # sh2['c' + str(int(r+2))].value = sh2['S' + str(int(r+1))].value
                        # sh2['R' + str(int(r+1))].value = sh2['R' + str(int(r))].value
                        # sh2['c' + str(int(r+1))].value = sh2['S' + str(int(r))].value
                        # sh2['R' + str(int(r))].value = myt
                        # sh2['c' + str(int(r))].value = st
                        time.sleep(0.2)

                    save_수익율2 = str(수익율)
                    # print(target_item)
                    # logging.info('- 최종 매수시간:' + str(last_buy_dt))

                    # print(Decimal(str(현재고점대비하락율)) , Decimal(str(dcnt_pcnt)))

                    # logging.info('시장가 매도 시작! [' + str(target_item['market']) + ']')
                                  # -0.09 <= -0.25
                    # print(Decimal(str(현재고점대비하락율)) , Decimal(str(dcnt_pcnt)))
                    #              현재의 고점대비하락율     <=  고점대비하락율
                    if Decimal(str(현재고점대비하락율)) <= Decimal(str(손절율)):
                        # print(Decimal(str(현재고점대비하락율)), Decimal(str(dcnt_pcnt)))
                        x = 1
                        # ------------------------------------------------------------------
                        # 시장가 매도
                        # 실제 매도 로직은 안전을 위해 주석처리 하였습니다.
                        # 실제 매매를 원하시면 테스트를 충분히 거친 후 주석을 해제하시면 됩니다.
                        # ------------------------------------------------------------------
                        # if str(target_item['market']) != 'KRW-ETH':
                        if str(target_item['market']) not in 'KRW-SHIBX':
                            logging.info('시장가 매도 시작! [' + str(target_item['market']) + ']')
                            #      print('모의 매도 함. : ',target_item['market'])
                            sh2['T' + str(int(19))].value = '모의 매도 함. : ', target_item['market']
                            time.sleep(0.2)

                            # rtn_sellcoin_mp = upbit.sellcoin_mp(target_item['market'], 'Y')
                            # logging.info(' 3. 시장가 매도 종료! [' + str(target_item['market']) + ']' + ' ' + str(ticker['trade_price']) + '<-- 매도 현재가 ')
                            # logging.info(rtn_sellcoin_mp)
                            # logging.info('------------------------------------------------------')

                            # wb = xw.Book.caller()
                            # sh2 = wb.sheets('4H')  # Worksheet 설정
                            myt = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            r = sh2['R19'].value

                            sh2['R' + str(int(r + 2))].value = sh2['R' + str(int(r + 1))].value
                            sh2['S' + str(int(r + 2))].value = sh2['S' + str(int(r + 1))].value
                            sh2['R' + str(int(r + 1))].value = sh2['R' + str(int(r))].value
                            sh2['S' + str(int(r + 1))].value = sh2['S' + str(int(r))].value
                            sh2['R' + str(int(r))].value = myt
                            sh2['S' + str(int(r))].value = st
                            time.sleep(0.2)

                    else:
                        x = 1
                        logging.info('- 고점 대비 하락률 조건에 맞지 않아 매도하지 않음!!!')
                        sh2['T' + str(int(19))].value = '고점 대비 하락률 조건에 맞지 않아 매도하지 않음!!!'
                        time.sleep(0.2)
                        # logging.info('------------------------------------------------------')

                time.sleep(0.2)
                print('매도 체크 : ', ticker['market'])
                # wb4 = xw.Book.caller()
                # sh4 = wb4.sheets('4H')  # Worksheet 설정
                sh2['T' + str(int(19))].value = ticker['market']
                # xxx

        sh2['T' + str(int(19))].value = '매도한 것 없음'
        time.sleep(0.2)
    # ---------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:

        raise


def up_called():  # 4  5분연속상승시 매수
    try:

        # log_level = input("로그레벨(D:DEBUG, E:ERROR, 그 외:INFO) : ").upper()
        # buy_amt = input("매수금액(M:최대, 10000:1만원) : ").upper()
        # upbit.set_loglevel("I")
        wb4 = xw.Book.caller()
        sh4 = wb4.sheets('4H')  # Worksheet 설정

        # ----------------------------------------------------------------------
        # 반복 수행
        # ----------------------------------------------------------------------
        # while True:

        # logging.info("*********************************************************")
        # logging.info("1. 로그레벨 : " + str(log_level))
        # logging.info("2. 매수금액 : " + str(buy_amt))
        # logging.info("*********************************************************")

        # -----------------------------------------------------------------
        # 전체 종목 리스트 추출
        # -----------------------------------------------------------------
        target_items = upbit.get_items('KRW', '')

        # -----------------------------------------------------------------
        # 종목별 체크
        # -----------------------------------------------------------------
        i = 0
        for target_item in target_items:
            rsi_val = False
            mfi_val = False
            ocl_val = False

            # logging.info('체크중....[' + str(target_item['market']) + ']')  # shin
            # print('체크중....[' + str(target_item['market']) + ']')
            # -------------------------------------------------------------
            # 종목별 보조지표를 조회
            # 1. 조회 기준 : 일캔들, 최근 5개 지표 조회
            # 2. 속도를 위해 원하는 지표만 조회(RSI, MFI, MACD, CANDLE)
            # - Input
            #   1) target_item : 대상 종목
            #   2) tick_kind : 캔들 종류 (1, 3, 5, 10, 15, 30, 60, 240 - 분, D-일, W-주, M-월)
            #   3) inq_range : 캔들 조회 범위
            #   4) loop_cnt : 지표 반복계산 횟수
            #   5) 보조지표 : 리스트
            # -------------------------------------------------------------
            # indicators = upbit.get_indicator_sel(target_item['market'], 'D', 200, 5,  # shin
            indicators = upbit.get_indicator_sel(target_item['market'], '1', 50, 5, ['CANDLE'])  # 1분 shinI
            #                            # ['RSI', 'MFI', 'MACD', 'CANDLE'])
            # print(indicators)
            # --------------------------------------------------------------
            # 최근 상장하여 캔들 갯수 부족으로 보조 지표를 구하기 어려운 건은 제외
            # --------------------------------------------------------------
            # if 'CANDLE' not in indicators or len(indicators['CANDLE']) < 200:
            #     logging.info('캔들 데이터 부족으로 데이터 산출 불가...[' + str(target_item['market']) + ']')
            #     continue

            # --------------------------------------------------------------
            # 보조 지표 추출
            # --------------------------------------------------------------
            # rsi = indicators['RSI']
            # mfi = indicators['MFI']
            # macd = indicators['MACD']
            candle = indicators['CANDLE']
            # print(indicators)
            # print(candle[0]['market'])
            # print(str(dt.datetime.now()))

            # 5연속 상승이면 매수한다.
            # if candle[0]['high_price'] > candle[1]['high_price'] > candle[2]['high_price'] > candle[3]['high_price'] >  candle[4]['high_price']:
            # 4연속 상승 으로 테스트 해 보장.
            if (candle[0]['high_price'] > candle[1]['high_price'] > candle[2]['high_price'] > candle[3]['high_price']) or (candle[0]['high_price'] < candle[1]['high_price'] < candle[2]['high_price'] < candle[3]['high_price']) :

                # play_5up(target_item['korean_name'] + " 연속 상승 중...")
                print(
                    '                                                                                                                                           연속상승 [' +
                    target_item['korean_name'] + ']',
                    round((candle[0]['low_price'] - candle[4]['low_price']) / candle[4]['low_price'] * 100, 2),
                    candle[0]['high_price'], candle[1]['high_price'], candle[2]['high_price'], candle[3]['high_price'],
                    candle[4]['high_price'], str(dt.datetime.now()))
                wb = xw.Book.caller()
                sh2 = wb.sheets('UP')  # Worksheet 설정

                myt = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                r = sh2['J1'].value
                # y = 0  # sh2['I1'].value  # 루핑...체크 1이면 돌고, 0이면 정지.
                sh2['A' + str(int(r))].value = myt
                sh2['B' + str(int(r))].value = target_item['korean_name']  # 지수
                sh2['C' + str(int(r))].value = round(
                    (candle[0]['low_price'] - candle[4]['low_price']) / candle[4]['low_price'] * 100, 2)  # 상승율
                sh2['D' + str(int(r))].value = dt.datetime.now().strftime("%H:%M:%S")
                sh2['E' + str(int(r))].value = target_item['korean_name']  # 지수
                sh2['F' + str(int(r))].value = round(
                    (candle[0]['low_price'] - candle[4]['low_price']) / candle[4]['low_price'] * 100, 2)  # 상승율

                # ------------------------------------------------------------------
                # 기매수 여부 판단
                # ------------------------------------------------------------------
                accounts = upbit.get_accounts('Y', 'KRW')
                account = list(filter(lambda x: x.get('market') == target_item['market'], accounts))

                # 이미 매수한 종목이면 다시 매수하지 않음
                # sell_bot.py에서 매도 처리되면 보유 종목에서 사라지고 다시 매수 가능
                if len(account) > 0:
                    logging.info('기 매수 종목으로 매수하지 않음....[' + str(target_item['korean_name']) + ']')
                    sh4['C' + str(int(6))].value = '기 매수 종목으로 매수하지 않음....[' + str(target_item['korean_name']) + ']'
                    time.sleep(0.2)
                    continue

                # ------------------------------------------------------------------
                # 매수금액 설정
                # 1. M : 수수료를 제외한 최대 가능 KRW 금액만큼 매수
                # 2. 금액 : 입력한 금액만큼 매수
                # ------------------------------------------------------------------
                buy_amt = 10100  # shin
                # buy_amt == 'M'
                available_amt = upbit.get_krwbal()['available_krw']

                if buy_amt == 'M':
                    buy_amt = available_amt

                # ------------------------------------------------------------------
                # 입력 금액이 주문 가능금액보다 작으면 종료
                # ------------------------------------------------------------------
                if Decimal(str(available_amt)) < Decimal(str(buy_amt)):
                    logging.info('주문 가능금액[' + str(available_amt) + ']이 입력한 주문금액[' + str(buy_amt) + '] 보다 작습니다.')
                    sh4['C' + str(int(6))].value = '주문 가능금액[' + str(available_amt) + ']이 입력한 주문금액[' + str(buy_amt) + '] 보다 작습니다.'
                    time.sleep(0.2)
                    continue

                # ------------------------------------------------------------------
                # 최소 주문 금액(업비트 기준 5000원) 이상일 때만 매수로직 수행
                # ------------------------------------------------------------------
                if Decimal(str(buy_amt)) < Decimal(str(upbit.min_order_amt)):
                    logging.info('주문금액[' + str(buy_amt) + ']이 최소 주문금액[' + str(upbit.min_order_amt) + '] 보다 작습니다.')
                    sh4['C' + str(int(6))].value = '주문금액[' + str(buy_amt) + ']이 최소 주문금액[' + str(upbit.min_order_amt) + '] 보다 작습니다.'
                    time.sleep(0.2)
                    continue

                # ------------------------------------------------------------------
                # 시장가 매수
                # 실제 매수 로직은 안전을 위해 주석처리 하였습니다.
                # 실제 매매를 원하시면 테스트를 충분히 거친 후 주석을 해제하시면 됩니다.
                # ------------------------------------------------------------------
                logging.info('시장가 매수 시작! [' + str(target_item['korean_name']) + ']')
                # rtn_buycoin_mp = upbit.buycoin_mp(target_item['market'], buy_amt)
                print('모의 매수함. : ', target_item['market'])
                sh4['C' + str(int(6))].value = '모의 매수함.' + target_item['korean_name']
                time.sleep(0.2)
                logging.info('시장가 매수 종료! [' + str(target_item['korean_name']) + ']')
                # logging.info(rtn_buycoin_mp)

                # --------------------------------------------------



            # print(candle[199]['market'])
            # --------------------------------------------------------------
            # 매수 로직
            # 1. RSI : 2일전 < 30미만, 3일전 > 2일전, 1일전 > 2일전, 현재 > 1일전
            # 2. MFI : 2일전 < 20미만, 3일전 > 2일전, 1일전 > 2일전, 현재 > 1일전
            # 3. MACD(OCL) : 3일전 < 0, 2일전 < 0, 1일전 < 0, 3일전 > 2일전, 1일전 > 2일전, 현재 > 1일전
            # --------------------------------------------------------------

            # --------------------------------------------------------------
            # RSI : 2일전 < 30미만, 3일전 > 2일전, 1일전 > 2일전, 현재 > 1일전
            # rsi[0]['RSI'] : 현재
            # rsi[1]['RSI'] : 1일전
            # rsi[2]['RSI'] : 2일전
            # rsi[3]['RSI'] : 3일전
            # --------------------------------------------------------------
            #  if (Decimal(str(rsi[0]['RSI'])) > Decimal(str(rsi[1]['RSI'])) > Decimal(str(rsi[2]['RSI']))
            #          and Decimal(str(rsi[3]['RSI'])) > Decimal(str(rsi[2]['RSI']))
            #          and Decimal(str(rsi[2]['RSI'])) < Decimal(str(30))):
            #      rsi_val = True
            # for 문의 아래부분
            # time.sleep(0.2)
            print('5연속상승 체크 : ', target_item['korean_name'])
            # wb4 = xw.Book.caller()
            # sh4 = wb4.sheets('4H')  # Worksheet 설정
            i = i + 1
            sh4['C' + str(int(6))].value = str(i) + ':' + str(i) + ' : ' + target_item['korean_name'] + ' : ' + str(round((candle[0]['low_price'] - candle[4]['low_price']) / candle[4]['low_price'] * 100, 2))
            time.sleep(0.01)


    # ---------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise


def ubmi_called():  # 3
    wb = xw.Book.caller()
    sh2 = wb.sheets('UBMI')  # Worksheet 설정
    step = "3"
    days = 1  # 최근 n일의 데이터 수집
    idx = "UBMI"  # 인덱스명
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # idx = "UBAI"  # 인덱스명
    url = "https://crix-api-cdn.upbit.com/v1/crix/candles/minutes/" + step + "?code=IDX.UPBIT." + idx + "&count=" + str(
        days)
    y = 1

    # while y == 1:
    data = requests.get(url).json()

    if data[0]['tradePrice'] >= data[0]['openingPrice']:
        rtn = "+"
    else:
        rtn = ""
    rtn = rtn + "{0:0.0f}%".format(
        (data[0]['tradePrice'] - data[0]['openingPrice']) / data[0]['openingPrice'] * 100 * 100)

    rtn2 = "{0:0.2f}".format(data[0]['tradePrice'])

    time.sleep(0.1)
    # dt.datetime.now()
    myt = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    r = sh2['J1'].value
    # y = 0  # sh2['I1'].value  # 루핑...체크 1이면 돌고, 0이면 정지.

    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sh2['A' + str(int(r))].value = myt
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sh2['B' + str(int(r))].value = rtn2  # 지수
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sh2['C' + str(int(r))].value = rtn  # 상승율
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sh2['D' + str(int(r))].value = dt.datetime.now().strftime("%H:%M:%S")
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sh2['E' + str(int(r))].value = rtn2  # 지수
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sh2['F' + str(int(r))].value = rtn  # 상승율
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def ixic_called():  # 2
    wb = xw.Book.caller()
    sh2 = wb.sheets('IXIC')  # Worksheet 설

    mandate = dt.datetime.now().strftime("%Y-%m-%d")
    df = fdr.DataReader('IXIC', '2023-02-10', mandate).reset_index()

    for r in range(len(df)):
        sh2['A' + str(int(r + 2))].value = df['Date'][r].strftime("%Y-%m-%d")
        sh2['B' + str(int(r + 2))].value = df['Close'][r]

    # wb.close()


def main_called():  # 1
    # s = ['minute1', 'minute3', 'minute5', 'minute10', 'minute15', 'minute30', 'minute60', 'minute240',
    # 'day'] ss = ['minute01', 'minute03', 'minute05', 'minute10', 'minute15', 'minute30', 'minute60', 'minuteH04',
    # 'minuteH24']

    # range(3) <---아래 부분 수정 필요 : 아래 항목수에 따라 .3개면 3
    s = ['minute240']
    ss = ['minuteH4']

    # excel = win32com.client.Dispatch("Excel.Application") #엑셀 프로그램 실행
    # excel.Visible = True #앞으로 실행과정을 보이게
    # wb = excel.Workbooks.Add()  # 엑셀 프로그램에 Workbook 추가(객체 설정)
    # wb = excel.Workbooks.Open(r"C:\Users\shineuiho\OneDrive\바탕 화면\어여자.xlsb")
    # ws = wb.Worksheets("New")  # Worksheet 설정

    # 셀 row, col 값 지정하여 값넣기(Range("A1")과 동일 함)
    # ws.cells(1, 1).Value = ws.cells(1, 1).Value

    # 샘플
    # wb = xw.Book.caller()
    # sheet = wb.sheets[0]
    # sheet["A1"].value = "xlwings 모듈 test"
    # sheet["A2"].value = "투손플레이스"

    # 엑셀 매크로파일 열기(path는 매크로 파일이 있는 경로)
    wb = xw.Book.caller()  # xw.Book(r"C:\upbit\trade_bot\어여자.xlsb")
    sh1 = wb.sheets('토')  # Worksheet 설정

    tt = dt.datetime.now()
    # print(tt, 'start')
    # print(pyupbit.get_tickers(fiat='KRW'))

    r = sh1['J1'].value  # 최종 엑셀 데이터 존재 행.
    for j in range(1):  # 9 # 0  8까지 : 시간 타입 (예 : minuteH24) '4개면 4개
        result = []

        for t in pyupbit.get_tickers(fiat='KRW', verbose=True):
            # print(t['market'], j, s[j],pyupbit.get_ohlcv(ticker=t['market'], count=1, interval=s[j])['value'].values[0])
            volumes = (t['market'], pyupbit.get_ohlcv(ticker=t['market'], count=1, interval=s[j])['value'].values[0],
                       t['korean_name'])
            result.append(volumes)
            time.sleep(0.2)  # 너무 빠르면 , 간혹 오류

        result.sort(key=lambda x: x[1])
        # print('result[-5:]====', result[-5:])

        x = 0
        for i in result[-100:]:
            r = r + 1
            x = x + 1
            # print(tt, ss[j], i[2], i[1], 11 - x)
            # print('A' + str(int(r)))
            sh1['A' + str(int(r))].value = tt
            sh1['B' + str(int(r))].value = tt
            sh1['C' + str(int(r))].value = ss[j]
            sh1['D' + str(int(r))].value = i[2]
            sh1['E' + str(int(r))].value = i[1]
            sh1['F' + str(int(r))].value = 101 - x
            sh1['G' + str(int(r))].value = tt.strftime("%d %H:%M")

    # 엑셀 VBA의 매크로 함수 'doit'를 파이썬 함수로 지정

    # macro_amt = wb.macro('amt')  # 피벗리프레시 및 그래프 셋팅
    # macro_call = wb.macro('chart10')  # 피벗리프레시 및 그래프 셋팅
    # macro_make5 = wb.macro('Table100')  # 상위 10등의 표 표시 : 십전팔기

    # VBA 함수 실행
    # macro_amt()
    # macro_call()
    # macro_make5()


    # wb.save()
    # wb.close
    # wb.quit()


def main(s='0'):
    xw.Book("top20.xlsb").set_mock_caller()
    print(s, 'main start ...')
    if s == '1':
        main_called()
    if s == '2':
        ixic_called()
    if s == '3':
        ubmi_called()
    if s == '4':
        up_called()
    if s == '5':
        sell_called()

    print(s, 'main end ... oops!')


if __name__ == "__main__":
    if sys.argv[1] == '1':
        # th1 = Thread(target=main, args='1', daemon=True)  # 거래금액
        # th1.start()
        p1 = Process(target=main, args='1')
        p1.start()
        # p1.join()

    if sys.argv[1] == '2':
        p2 = Process(target=main, args='2')  # 나스닥
        p2.start()
        # p2.join()
    if sys.argv[1] == '3':
        p3 = Process(target=main, args='3')  # 마켓지수
        p3.start()
        # p3.join()
    if sys.argv[1] == '4':
        p4 = Process(target=main, args='4')  # 5연속시 매수
        p4.start()
        # p4.join()
    if sys.argv[1] == '5':
        p5 = Process(target=main, args='5')  # 매도
        p5.start()
        # p5.join()

    # th1 = Thread(target=main, args='1')  # 거래금액
    # th1.start()

    # th2 = Thread(target=main, args='2')  # 나스닥
    # th2.start()

    # th3 = Thread(target=main, args='3')  # 마켓인덱스
    # th3.start()

    # th4 = Thread(target=main, args='4')  # 5연속시 매수 : up_called
    # th4.start()

    # th5 = Thread(target=main, args='5')  # 매도        : sell_called
    # th5.start()

    # 최종 물건......