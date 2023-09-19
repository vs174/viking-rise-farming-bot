# Foraging in Viking Rise
# Logic: If there are 3/3 heroes dispatched, every 10 minutes. Check if any heroes have returned. -> Automatically calculates time to prevent unnecessary consumption of resources.
# If a hero returns from dispatch, click the magnifying glass to proceed with dispatch.
import datetime as dt
import random
import time
import pyautogui

import cv2
import numpy as np
import pytesseract

# from PIL import Image
# import pytesseract

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True


def delay_time(delay_second):  # 시간 딜레이
    time.sleep(delay_second)


def image_to_string():

    time.sleep(0)

    # Get the width and height of the right monitor.
    right_monitor_width = pyautogui.size()[0]
    right_monitor_height = pyautogui.size()[1]
    # print(right_monitor_width)
    # print(right_monitor_height)
    # Capture the screen of the right monitor.
    screenshot_path = 'screenshot_time.png'
    # 이미지 저장
    pyautogui.screenshot(screenshot_path, region=(right_monitor_width / 2.35, right_monitor_height / 5, right_monitor_width
                                                  / 16, right_monitor_height / 1.5))
    screenshot_image = cv2.imread(screenshot_path)

    text_time = pytesseract.image_to_string(screenshot_image)

    return text_time


def save_screenshot(every_second):
    delay_time(every_second)
    # print_timestamp('screenshot')
    # 왼쪽 모니터의 너비와 높이
    left_monitor_width = pyautogui.size()[0]
    left_monitor_height = pyautogui.size()[1]
    # 왼쪽 모니터의 화면 캡처
    pyautogui.screenshot('screenshot.png', region=(0, 0, left_monitor_width, left_monitor_height))
    # print_timestamp('screenshot ---- end')
    # delay_time(every_second)


def get_min_time():   #Find the minimum time
    try:
        min_times = 3600 * 24  # 24시간
        time_count = 0  #Number of units = Number of return times for each unit.
        min_time_text = '00:00:00'
        later_time_text = '00:00:00'
        hms = ''

        try_cnt = 0
        txt = ['00:00:02']
        while try_cnt <= 10:  #Retry 10 times. Number recognition, 4*2 list array
            text_time = image_to_string()  #Save time from images.
            txt = text_time.split('\n')
            try_cnt = try_cnt + 1
            if len(txt) == 8:
                break

        print_timestamp('------->')
        if len(txt) == 8:  # If the marching arrangement is 4*2, all of them have been read.
            for tx in txt:
                if tx != '':
                    # print_timestamp(tx)
                    # print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tx, end=' ')
                    print(dt.datetime.now().strftime("%I:%M:%S"), tx, end=' ')

                    if len(tx) == 8:
                        time_count = time_count + 1
                        tx = tx.replace("O", "0")
                        hms = tx
                        h = int(hms[0:2])
                        m = int(hms[3:5])   #error
                        s = int(hms[6:8])
                        # print(h,m,s)
                        t = h * 60 * 60 + m * 60 + s
                        if t < min_times:
                            min_times = t  # Shortest time to return to unit converted to seconds
                            min_time_text = tx  # 부대 복귀 최단 시간 텍스트
                            # print_timestamp(str(tx) + '   ' + str(min_times) )
                            print('   ' + str(min_times), end='\n')
                            now = dt.datetime.now()
                            later_time_text = now + dt.timedelta(seconds=t + 2)  # 2 : 0초인 경우 대비 해서. 2초 둠.
                        else:
                            print('   ', end='\n')

            print_timestamp("------->")

        return min_times + 60, time_count, min_time_text, later_time_text  # 60 : 0초인 경우 대비 해서. 60초 둠.

    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception as e:
        print(e)
        # 예외가 발생한 경우 실행할 코드
        return 0 + 2, 4, min_time_text, later_time_text


def scroll_down(x,y): # 현재 안씀.
    # 부대가 4이상이 되면 하단이 안보임. 그래서 보정 : 부대 보기 화면을 한 행 내린다.
    time.sleep(0.5)
    # pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

    # 컨트롤 키를 누릅니다.
    pyautogui.keyDown("control")

    # 아래 화살표 키를 누릅니다.
    pyautogui.keyDown("down")

    # 컨트롤 키를 뗍니다.
    pyautogui.keyUp("control")

    # 아래 화살표 키를 뗍니다.
    pyautogui.keyUp("down")


def print_timestamp(msg):
    # print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(dt.datetime.now().strftime("%I:%M:%S"), msg)


def click_button(screenshot_image_gray, array_find_button):
    # 화면 캡처 이미지 로드
    # screenshot_image = cv2.imread('screenshot.png')
    # screenshot_image_gray = cv2.cvtColor(screenshot_image, cv2.COLOR_BGR2GRAY)

    # 찾을 버튼 이미지 로드
    # print_timestamp("                     find button --------- start")
    for find_button in array_find_button:

        # 채굴 대상 랜덤 선택(영지 근처에 자원이 없는 경우가 자주 있음.)
        find_button_image = cv2.imread(find_button + '.png')
        find_image_gray = cv2.cvtColor(find_button_image, cv2.COLOR_BGR2GRAY)
        # button_width, button_height = find_image_gray.shape[::-1]

        # 버튼 이미지 매칭
        result = cv2.matchTemplate(screenshot_image_gray, find_image_gray, cv2.TM_CCOEFF_NORMED)

        # 버튼과 일치 하는 이미지의 위치 찾기
        threshold = 0.9

        location = np.where(result >= threshold)

        # 버튼 이미지를 찾았다면
        if len(location[0]) > 0:
            # 첫 번째 일치하는 위치 가져오기
            # x, y = (location[1][0] + 5, location[0][0] + 5)  # 10픽셀 우측, 아래로'
            x, y = (location[1][0] + 0, location[0][0] + 0)  # 10픽셀 우측, 아래로'
            pyautogui.click(x, y, button='left', clicks=1, interval=0.1)
            break
    pyautogui.click(1, 1, button='left', clicks=1, interval=0.1)


def find_and_click_button(array_find_button):
    delay_time(0.1)
    history = ""
    for find_button in array_find_button:
        history = find_button
        # print_timestamp("=" * 12 + history)
        # 채굴 대상 랜덤 선택(영지 근처에 자원이 없는 경우가 많음.)
        if find_button == "./imgs/02_cj_ssj_dbg_gdgs" or find_button == "./imgs/02_cj_ssj_dbg_csj" or find_button == "./imgs/02_cj_ssj_dbg_bmj" or find_button == "./imgs/02_cj_ssj_dbg_nj":
            # find_button = random.choice(["02_cj_ssj_dbg_gdgs", "02_cj_ssj_dbg_csj", "02_cj_ssj_dbg_bmj", "02_cj_ssj_dbg_nj", "02_cj_ssj_dbg_nprdj"])
            find_button = random.choice(
                ["./imgs/02_cj_ssj_dbg_nj", "./imgs/02_cj_ssj_dbg_nj", "./imgs/02_cj_ssj_dbg_nj", "./imgs/02_cj_ssj_dbg_nj"])  # 니풀롱일족은 제거함. 에러발생으로, 02_cj_ssj_dbg_gdgs 2번으로 조정함...

        # 버튼을 찾는다.
        found_button = pyautogui.locateOnScreen(find_button + ".png", confidence=0.9, region=(0, 0, 2560 - 10 , 1600 - 10 ))
        # print('찾는 중', find_button)
        if found_button is not None:
            # print(found_button)
            x, y, w, h = found_button

            # 첫 번째 일치하는 위치 가져오기
            # x, y = (location[1][0] + 5, location[0][0] + 5)  # 10픽셀 우측, 아래로'
            # x, y = (location[1][0] + 0, location[0][0] + 0)  # 10픽셀 우측, 아래로'

            print_timestamp(" " * 12 + find_button)

            # 출동 완료 : 부대 보기 화면 으로 이동 준비
            if find_button == "01_cj_44":
                # delay_time(2)  # 2초후 부터 행군 완료 대기.

                # 화살표 클릭 : 부대 보기 화면 전환
                # find_buttons2 = ['03_cj_44_arrow']
                # find_and_click_button(find_buttons2)

                # 부대보기 화면으로 이동
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)
                # 부대가 4이상이 되면 하단이 안보임. 그래서 보정 : 부대 보기 화면을 한 행 내린다.
                time.sleep(0.1)
                # pyautogui.click(500, 500, button='left', clicks=1, interval=0.1)
                # 마우스를 100픽셀 아래로 스크롤합니다.
                pyautogui.scroll(-100)

                # 부대 보기 : 최소 시간 추출
                time_cnt = 0
                extracted_second = 2
                later_time_text ='00:00:00'
                extracted_time_text = '00:00:00'

                # 문자인식 : 행군예정시간 4개이면 대기, 그렇지 않으면 루프
                extracted_second, time_cnt, extracted_time_text, later_time_text = get_min_time()

                # 무조건 X 를 눌러서 빠져나온다.
                # save_screenshot(0.1)
                # find_buttons2 = ['02_cj_cross']
                # click_button(screenshot_image_gray, find_buttons2)

                # 4개의 시간을 인식하면 딜레이 시간을 준다.
                if time_cnt == 4:
                    print_timestamp(str(time_cnt) + "개의 부대가 모두 출동 하였습니다.")
                    print_timestamp("복귀시간 : " + extracted_time_text)
                    print_timestamp("복귀시각 : "  + str(later_time_text.strftime("%I:%M:%S")))
                    # 화살표 클릭 : 부대 보기 화면 전환
                    pyautogui.click(1, 100, button='left', clicks=1, interval=0.1)  # 부대보기 화면 닫고. 대기.
                    delay_time(extracted_second)   # 계산된 시간 만큼 기다린다.
                break

            # 자원 채집 버튼들
            elif find_button == "./imgs/02_cj_ssj_dbg_gdgs" or find_button == "./imgs/02_cj_ssj_dbg_csj" or find_button == "./imgs/02_cj_ssj_dbg_bmj" or find_button == "./imgs/02_cj_ssj_dbg_nj" or find_button == "./imgs/02_cj_ssj_dbg_nprdj" or find_button == "./imgs/02_cj_ssj_dbg_mst":
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)  # 자원 버튼 클릭
                pyautogui.click(x, y - 200, button='left', clicks=1, interval=0.1)  # 검색 버튼 클릭, -100 : 자원버튼 위의 검색 버튼
                # print_timestamp("." * 10 + find_button)
                break

            elif find_button == "./imgs/02_cj_ssj_dbg_gs_cj_ss_cd_hg_star":
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)
                # 마우스를 1000 위로 스크롤합니다.
                pyautogui.click(x=1, y=500, button='left', clicks=1, interval=1)  # 족장 얼굴로 전환 해서 빠져 나오기
                pyautogui.scroll(500)
                print('더블 행군 방지를 위하여 이동.')
                break

            elif find_button == "./imgs/02_cj_ssj_dbg_gs_cj_ss":
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)
                # print_timestamp("~" * 10 + find_button)
                break

            elif find_button == "./imgs/02_cj_ssj_two_sohan":
                # 마우스를 100픽셀 위로 스크롤합니다.
                pyautogui.scroll(100)
                pyautogui.click(x=1, y=1, button='left', clicks=1, interval=0.1) # 족장 얼굴로 전환 해서 빠져 나오기
                break

            elif find_button == "./imgs/02_cj_ssj_move_del":
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1) # 자기 삭제하고.
                pyautogui.click(x + 200, y, button='left', clicks=1, interval=0.1) # 200 : 동일화면 이동하기 클릭
                break

            elif find_button == "./imgs/02_cj_cross":
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)
                # 마우스를 100픽셀 위로 스크롤합니다.
                pyautogui.scroll(100)
                break

            elif find_button == "./imgs/02_cj_ssj_two":

                found_button = pyautogui.locateOnScreen(find_button + ".png", confidence=0.8,
                                                        region=(500, 500, 2560 - 500, 1600 - 500))
                if found_button is not None:
                    pyautogui.click(found_button)
                else:
                    offset_y = random.choice([200, 400, 600, 800, 1000, 1200, 1400])
                    pyautogui.click(x, offset_y, button='left', clicks=1, interval=0.1)
                    pyautogui.scroll(100)
                # offset_y = random.choice([0, 0, 0, 0, 0, 200, 100])

                # pyautogui.click(x, y + offset_y, button='left', clicks=1, interval=0.1)
                # 마우스를 100픽셀 위로 스크롤합니다.
                # pyautogui.scroll(100)
                break

            # 이동 버튼들
            else:  # 찾은 버튼을 클릭
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)
                # print_timestamp("일" * 10 + find_button)
                break

    return history
    # print_timestamp("                     find button --------- end")

# main-------------------------------------------------------------------------------------------------------------------
try:

    prev_button = ""
    same_button_cnt = 0
    while True:
        # 5초마다 screenshot 찍어 저장
        # save_screenshot(0.1)

        find_buttons = [
                        './imgs/04_cj_cancel',
                        './imgs/04_cj_confirm',
                        './imgs/02_cj_back',
                        './imgs/01_cj_44',
                        './imgs/02_cj_ssj_dbg_gs_cj_ss_cd_hg',
                        './imgs/02_cj_cross',
                        './imgs/02_cj_ssj_dbg_gs_cj_ss',
                        './imgs/02_cj_ssj_dbg_gs_cj',

                        './imgs/02_cj_ssj_dbg_bmj',
                        './imgs/02_cj_ssj_dbg',

                        './imgs/02_cj_ssj',
                        './imgs/02_cj_yj'
                        ]
        find_buttonsX = [
                        './imgs/04_cj_cancel',
                        './imgs/04_cj_confirm',
                        './imgs/02_cj_back',
                        './imgs/01_cj_44',
                        './imgs/02_cj_ssj_dbg_gs_cj_ss_cd_hg_star',

                        './imgs/02_cj_ssj_dbg_gs_cj_ss',
                        './imgs/02_cj_ssj_dbg_gs_cj',

                        './imgs/02_cj_ssj_two_sohan',
                        './imgs/02_cj_ssj_two',
                        './imgs/02_cj_ssj_move_del',
                        './imgs/02_cj_ssj_star',
                        './imgs/02_cj_cross',

                        './imgs/02_cj_ssj',
                        './imgs/02_cj_yj'
                        ]
        if random.choice(['near','far']) == "near":
            cur_button = find_and_click_button(find_buttons)
        else:
            cur_button = find_and_click_button(find_buttons)

        # print('반환된 버튼', cur_button)
        if prev_button == "":
            prev_button = cur_button
            same_button_cnt = same_button_cnt + 1
        elif prev_button == cur_button:   # 무한 루프 조짐.
            same_button_cnt = same_button_cnt + 1
        else:
            prev_button = cur_button
            same_button_cnt = 0
        # print(str(same_button_cnt), prev_button, cur_button)

        # 3회 이상 동일한 메시지가 나오면 빈 공간을 클릭하고, 100픽셀 위로 올린다.
        if same_button_cnt == 3:
            print_timestamp(" " * 12 + '무한 루프 해결')

            print(str(same_button_cnt), prev_button, cur_button)

            found_button = pyautogui.locateOnScreen("./imgs/02_cj_cross.png", confidence=0.9,
                                                    region=(500, 500, 2560 - 500, 1600 - 500))
            if found_button is not None:
                pyautogui.click(found_button)

            random_y = random.choice([400, 800])
            pyautogui.click(x=2, y=random_y, button='left', clicks=1, interval=0.1)   # 탈출
            pyautogui.scroll(100)
            prev_button = ""
            same_button_cnt = 0
        

# ---------------------------------------
# 모든 함수의 공통 부분(Exception 처리)
# ----------------------------------------
except Exception:
    raise
