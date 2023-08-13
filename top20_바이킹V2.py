# 바이킹 라이즈의 채집
# 로직 : 파견나간 영웅이 3/3이면 10분마다. 돌아온 영웅이 있는지 체크한다. -> 자동으로 시간계산을 해서 불필요한 리소스의 소모를 막는다.
# 파견에서 돌아온 영웅이 있으면, 돋보기를 눌러서 파견까지 진행한다.
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

    # 오른쪽    모니터의    너비와    높이를    가져옵니다.
    right_monitor_width = pyautogui.size()[0]
    right_monitor_height = pyautogui.size()[1]
    # print(right_monitor_width)
    # print(right_monitor_height)
    # 오른쪽    모니터의    화면을    캡처합니다.
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


def get_min_time():   # 최소시간 구하기
    try:
        min_times = 3600 * 24  # 24시간
        time_count = 0  # 부대의 갯수 = 각각의 부대의 복귀 시간의 갯수.
        min_time_text = '00:00:00'
        later_time_text = '00:00:00'
        hms = ''

        try_cnt = 0
        txt = ['00:00:02']
        while try_cnt <= 10:  # 10번 재 시도. 숫자 인식 , 4*2 개의 리스트 배열
            text_time = image_to_string()  # 이미지에서 시간을 구해낸다.
            txt = text_time.split('\n')
            try_cnt = try_cnt + 1
            if len(txt) == 8:
                break

        print_timestamp('------->')
        if len(txt) == 8:  # 행군배열이 4*2개이면 모두 읽은 것임.
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
                            min_times = t  # 부대 복귀 최단 시간 초 환산
                            min_time_text = tx  # 부대 복귀 최단 시간 텍스트
                            # print_timestamp(str(tx) + '   ' + str(min_times) )
                            print('   ' + str(min_times), end='\n')
                            now = dt.datetime.now()
                            later_time_text = now + dt.timedelta(seconds=t + 2)  # 2 : 0초인 경우 대비 해서. 2초 둠.
                        else:
                            print('   ', end='\n')

            print_timestamp("------->")

        return min_times + 2, time_count, min_time_text, later_time_text  # 2 : 0초인 경우 대비 해서. 2초 둠.

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

        # 채굴 대상 랜덤 선택(영지 근처에 자원이 없는 경우가 자주 있어서리.)
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
    # 화면 캡처 이미지 로드
    screenshot_image = cv2.imread('screenshot.png')
    screenshot_image_gray = cv2.cvtColor(screenshot_image, cv2.COLOR_BGR2GRAY)

    # 찾을 버튼 이미지 로드
    # print_timestamp("                     find button --------- start")
    history = ""
    for find_button in array_find_button:
        history = find_button
        # 채굴 대상 랜덤 선택(영지 근처에 자원이 없는 경우가 자주 있어서리.)
        if find_button == "02_cj_ssj_dbg_gdgs" or find_button == "02_cj_ssj_dbg_csj" or find_button == "02_cj_ssj_dbg_bmj" or find_button == "02_cj_ssj_dbg_nj":
            find_button = random.choice(["02_cj_ssj_dbg_gdgs", "02_cj_ssj_dbg_csj", "02_cj_ssj_dbg_bmj", "02_cj_ssj_dbg_nj", "02_cj_ssj_dbg_nprdj"])
        # print_timestamp(" " * 10 + find_button)
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

            print_timestamp(" " * 12 + find_button)

            # 출동 완료 : 부대 보기 화면 으로 이동 준비
            if find_button == "01_cj_44":
                # delay_time(2)  # 2초후 부터 이제나 저제나 행군 완료를 기다 린다.

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
            elif find_button == "02_cj_ssj_dbg_gdgs" or find_button == "02_cj_ssj_dbg_csj" or find_button == "02_cj_ssj_dbg_bmj" or find_button == "02_cj_ssj_dbg_nj" or find_button == "02_cj_ssj_dbg_nprdj" or find_button == "02_cj_ssj_dbg_mst":
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)  # 자원 버튼 클릭
                pyautogui.click(x, y - 200, button='left', clicks=1, interval=0.1)  # 검색 버튼 클릭, -100 : 자원버튼 위의 검색 버튼
                # print_timestamp("." * 10 + find_button)

            elif find_button == "02_cj_ssj_dbg_gs_cj_ss_cd_hg_star":
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)
                # 마우스를 100픽셀 위로 스크롤합니다.
                pyautogui.scroll(100)
                break

            elif find_button == "02_cj_ssj_two_sohan":
                # 마우스를 100픽셀 위로 스크롤합니다.
                pyautogui.scroll(100)
                pyautogui.click(x=1, y=1, button='left', clicks=1, interval=0.1) # 족장 얼굴로 전환 해서 빠져 나오기
                break

            elif find_button == "02_cj_ssj_move_del":
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1) # 자기 삭제하고.
                pyautogui.click(x + 200, y, button='left', clicks=1, interval=0.1) # 200 : 동일화면 이동하기 클릭
                break

            elif find_button == "02_cj_cross":
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1) # 자기 삭제하고.
                # 마우스를 100픽셀 위로 스크롤합니다.
                pyautogui.scroll(100)
                break

            elif find_button == "02_cj_ssj_two": #  낼 여기 부터 ...
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1) # 자기 삭제하고.

                offset_y = random.choice([0, 0, 0, 0, 0, 200, 100])

                pyautogui.click(x, y + offset_y, button='left', clicks=1, interval=0.1)  # 자기 삭제하고.
                # 마우스를 100픽셀 위로 스크롤합니다.
                pyautogui.scroll(100)
                break

            # 이동 버튼들
            else:  # 찾은 버튼을 클릭
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)
                # print_timestamp(" " * 10 + find_button)
                break

    return history
    # print_timestamp("                     find button --------- end")

# main-------------------------------------------------------------------------------------------------------------------
try:
    prev_button = ""
    same_button_cnt = 0
    while True:
        cur_button = ""
        # 5초마다 screenshot 찍어 저장
        save_screenshot(0.1)

        find_buttons = [
                        '04_cj_cancel',
                        '04_cj_confirm',
                        '02_cj_back',
                        '01_cj_44',
                        '02_cj_ssj_dbg_gs_cj_ss_cd_hg',
                        '02_cj_cross',
                        '02_cj_ssj_dbg_gs_cj_ss',
                        '02_cj_ssj_dbg_gs_cj',

                        '02_cj_ssj_dbg_bmj',
                        '02_cj_ssj_dbg',

                        '02_cj_ssj',
                        '02_cj_yj'
                        ]
        find_buttonsX = [
                        '04_cj_cancel',
                        '04_cj_confirm',
                        '02_cj_back',
                        '01_cj_44',
                        '02_cj_ssj_dbg_gs_cj_ss_cd_hg_star',

                        '02_cj_ssj_dbg_gs_cj_ss',
                        '02_cj_ssj_dbg_gs_cj',

                        '02_cj_ssj_two_sohan',
                        '02_cj_ssj_two',
                        '02_cj_ssj_move_del',
                        '02_cj_ssj_star',
                        '02_cj_cross',

                        '02_cj_ssj',
                        '02_cj_yj'
                        ]
        cur_button = find_and_click_button(find_buttons)


        if prev_button == "":
            prev_button = cur_button
            same_button_cnt = same_button_cnt + 1
        elif prev_button == cur_button:   # 무한 루프 조짐.
            same_button_cnt = same_button_cnt + 1
        else:
            prev_button = cur_button
            same_button_cnt = 1
        # print(str(same_button_cnt), prev_button, cur_button)

        if same_button_cnt == 3:
            print_timestamp("무한루프 시간")

            print(str(same_button_cnt), prev_button, cur_button)
            pyautogui.click(x=2, y=2, button='left', clicks=1, interval=0.1)   # 탈출
            prev_button = ""
            same_button_cnt = 0
        # 3회 이상 동일한 메시지가 나오면 무언가 처리한다.

# ---------------------------------------
# 모든 함수의 공통 부분(Exception 처리)
# ----------------------------------------
except Exception:
    raise
