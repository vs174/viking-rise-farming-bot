# 바이킹 라이즈의 채집
# 로직 : 파견나간 영웅이 3/3이면 10분마다. 돌아온 영웅이 있는지 체크한다. -> 자동으로 시간계산을 해서 불필요한 리소스의 소모를 막는다.
# 파견에서 돌아온 영웅이 있으면, 돋보기를 눌러서 파견까지 진행한다.
import datetime as dt
import time
import pyautogui
import mss

import cv2
import numpy as np
# from PIL import Image
# import pytesseract

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

def capture_and_recognize_image(template_image_path):
    time.sleep(0.1)

     # 오른쪽    모니터의    너비와    높이를    가져옵니다.
    right_monitor_width = pyautogui.size()[0]
    right_monitor_height = pyautogui.size()[1]
    # print(right_monitor_width)
    # print(right_monitor_height)
    # 오른쪽    모니터의    화면을    캡처합니다.
    pyautogui.screenshot('screenshot.png', region=(0, 0, right_monitor_width, right_monitor_height))

    # 이미지 저장
    screenshot_path = 'screenshot.png'
    # screenshot.save(screenshot_path)

    # 템플릿 이미지 로드
    template_image = cv2.imread(template_image_path)
    template_image_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
    # template_width, template_height = template_image_gray.shape[::-1]

    # 화면 캡처 이미지 로드
    screenshot_image = cv2.imread(screenshot_path)
    screenshot_image_gray = cv2.cvtColor(screenshot_image, cv2.COLOR_BGR2GRAY)

    # 이미지 매칭
    result = cv2.matchTemplate(screenshot_image_gray, template_image_gray, cv2.TM_CCOEFF_NORMED)

    # 일치하는 위치 찾기
    threshold = 0.9
    location = np.where(result >= threshold)

    # 일치하는 이미지가 발견되었는지 확인
    if len(location[0]) > 0:
        # 첫 번째 일치하는 위치 가져오기
        top_left = (location[1][0], location[0][0])
        # bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

        # 이미지에 사각형 그리기
        # cv2.rectangle(screenshot_image, top_left, bottom_right, (0, 255, 0), 2)

        # 인식된 이미지를 포함한 캡처 이미지 저장
        # recognized_image_path = 'recognized_image.png'
        # cv2.imwrite(recognized_image_path, screenshot_image)

        # 결과 반환
        # return recognized_image_path
        # x = top_left.split(',')[0]
        # y = top_left.split(',')[1]
        # x = int(str(x).replace('(', '').replace(' ', ''))
        # y = int(str(y).replace(')', '').replace(' ', ''))
        print(template_image_path, '---------------------->클릭', location[1][0], location[0][0])

        # text = pytesseract.image_to_string(screenshot_image)
        # print(text)

        return location[1][0], location[0][0]

    # 일치하는 이미지가 없을 경우 None 반환
    print(template_image_path, '없음')
    return '채집가능', 1

# 5. 채집
while True:
    time.sleep(1)

    # 3/3 체크( 없음, 1/3, 2/3이면 채집가능)
    x, y = capture_and_recognize_image('01_cj_33.png')

    if x == '채집가능':  # 3/3이 아니면 채집가능, 망치일때는 검색 안됨. 쌍십자가 있는지 찾아서 클릭하면, 영지 상태로 바뀜.
        x, y = capture_and_recognize_image('02_cj_yj.png')
        pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

        if x == 1:  # 쌍십자를 못찾았으면, 영지 상태이므로, 돋보기 클릭 가능.
            time.sleep(3)
            x, y = capture_and_recognize_image('02_cj_ssj_dbg.png')
            pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

            if x != 1:  # 돋보기를 클릭후, 채석장 , 검색
                # 채석장 : 없는 자원종류
                x, y = capture_and_recognize_image('02_cj_ssj_dbg_bmj.png')  # 02_cj_ssj_dbg_csj
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                # 검색
                x, y = capture_and_recognize_image('02_cj_ssj_dbg_gs.png')
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                # 채집가능 여부
                time.sleep(3)
                x, y = capture_and_recognize_image('02_cj_ssj_dbg_gs_cj.png')
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                while x == 1:  #채집 불가능시 루프
                    # 돋보기
                    x, y = capture_and_recognize_image('02_cj_ssj_dbg.png')
                    pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                    # 벌목장 : 없는 자원종류
                    x, y = capture_and_recognize_image('02_cj_ssj_dbg_nj.png')  # 02_cj_ssj_dbg_bmj
                    pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                    # 검색
                    x, y = capture_and_recognize_image('02_cj_ssj_dbg_gs.png')
                    pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                    # 채집가능
                    time.sleep(3)
                    x, y = capture_and_recognize_image('02_cj_ssj_dbg_gs_cj.png')
                    pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                    while x == 1:  # 채집 불가능시 루프
                        # 돋보기
                        x, y = capture_and_recognize_image('02_cj_ssj_dbg.png')
                        pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                        # 농장 : 없는 자원종류
                        x, y = capture_and_recognize_image('02_cj_ssj_dbg_bmj.png')
                        pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                        # 검색
                        x, y = capture_and_recognize_image('02_cj_ssj_dbg_gs.png')
                        pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                        # 채집가능
                        time.sleep(3)
                        x, y = capture_and_recognize_image('02_cj_ssj_dbg_gs_cj.png')
                        pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                        while x == 1:  # 채집 불가능시 루프
                            # 돋보기
                            x, y = capture_and_recognize_image('02_cj_ssj_dbg.png')
                            pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                            # 골드광산 : 없는 자원종류
                            x, y = capture_and_recognize_image('02_cj_ssj_dbg_gdgs.png')
                            pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                            # 검색
                            x, y = capture_and_recognize_image('02_cj_ssj_dbg_gs.png')
                            pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

                            # 채집가능
                            time.sleep(3)
                            x, y = capture_and_recognize_image('02_cj_ssj_dbg_gs_cj.png')
                            pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

            # 생성
            time.sleep(3)
            x, y = capture_and_recognize_image('02_cj_ssj_dbg_gs_cj_ss.png')
            pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

            # 최대
            time.sleep(3)
            x, y = capture_and_recognize_image('02_cj_ssj_dbg_gs_cj_ss_cd.png')
            pyautogui.click(x, y, button='left', clicks=1, interval=0.1)

            # 행군
            x, y = capture_and_recognize_image('02_cj_ssj_dbg_gs_cj_ss_cd_hg.png')
            pyautogui.click(x, y, button='left', clicks=1, interval=0.1)
    else:  # 33이면.
        # 33화살표
        # x, y = capture_and_recognize_image('03_cj_33_arrow.png')
        # pyautogui.click(x, y, button='left', clicks=1, interval=120)  # 이동 시간 고려 최대 : 120초

        print('10분간 대기중', dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(60*10)  # 10분

    # 타겟 파일 조각들
    # 02_cj_ssj.png
    # 02_cj_ssj_dbg.png
    # 02_cj_ssj_dbg_bmj.png
    # 02_cj_ssj_dbg_csj.png
    # 02_cj_ssj_dbg_gdgs.png
    # 02_cj_ssj_dbg_gs.png
    # 02_cj_ssj_dbg_gs_cj.png
    # 02_cj_ssj_dbg_gs_cj_ss.png
    # 02_cj_ssj_dbg_gs_cj_ss_cd.png
    # 02_cj_ssj_dbg_gs_cj_ss_cd_hg.png
    # 02_cj_ssj_dbg_mst.png
    # 02_cj_ssj_dbg_nj.png
    # 02_cj_ssj_dbg_nprdj.png
    # 02_cj_yj.png

    # while True:
    #
    #     time.sleep(3)
    #     # 화면 캡처
    #     monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}  # 캡처할 화면의 크기와 위치를 지정
    #     with mss.mss() as sct:
    #         image = np.array(sct.grab(monitor))
    #     # 픽셀 값 가져 오기
    #     pixel_value = image[357, 1825]  # y , x
    #     print(pixel_value)
    #     val = str(pixel_value) not in '[121 163  55 255][ 47  47 179 255][105 171 208 255]'
    #     if val:
    #         break

###############################

        # [121 163  55 255] 이동중
        # [ 47  47 179 255] 전투중
        # [105 171 208 255] 복귀중
        # [66 142 125 255]  복귀완료 (잔디색)
        # time.sleep(180)
###############################


# import pyautogui
# import time
# ## 1. 좌표 얻기(작동 기록)
# while True:
#     time.sleep(5)
#     # Get the mouse coordinates
#     x, y = pyautogui.position()
#
#     # Print the coordinates
#     print('pyautogui.click(', str(x), ',', str(y), ', button=', "'left',", 'clicks=1, interval=0.1)')
#


# import mss
# import numpy as np
#
# with mss.mss() as sct:
#
# 2. 화면의 특정 픽셀의 값 구하기.
#     monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}  # 캡처할 화면의 크기와 위치를 지정
#     image = np.array(sct.grab(monitor))
#     # 픽셀 값 가져오기
#     pixel_value = image[357, 1825]  # y , x
#     print(pixel_value)

    # [121 163  55 255] 이동중
    # [ 47  47 179 255] 전투중
    # [105 171 208 255] 복귀중
    # [66 142 125 255]  복귀완료 (잔디색)

# Main ----------------------
# 3. 나폴롱 공격 전용. 할수록 손행 .
# while True:
#     time.sleep(3)
#
#     pyautogui.click(374, 709, button='left', clicks=1, interval=3)
#     pyautogui.click(658, 635, button='left', clicks=1, interval=3)
#     pyautogui.click(1468, 654, button='left', clicks=1, interval=3)
#     pyautogui.click(1473, 259, button='left', clicks=1, interval=3)
#     pyautogui.click(1492, 804, button='left', clicks=1, interval=3)
#
#     while True:
#
#         time.sleep(3)
#         # 화면 캡처
#         monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}  # 캡처할 화면의 크기와 위치를 지정
#         with mss.mss() as sct:
#             image = np.array(sct.grab(monitor))
#         # 픽셀 값 가져오기
#         pixel_value = image[357, 1825]  # y , x
#         print(pixel_value)
#         val = str(pixel_value) not in '[121 163  55 255][ 47  47 179 255][105 171 208 255]'
#         if val:
#             break

# 4. 정보길드 미션수행
# while True:
#     time.sleep(3)
#
#     pyautogui.click(465, 712, button='left', clicks=1, interval=3)
#
#     coord_string = capture_and_recognize_image('01_정보길드_앞코_흑색.png')  # 정보길드 미션수행
#     print(coord_string)
#     x = coord_string.split(',')[0]
#     y = coord_string.split(',')[1]
#     x = int(str(x).replace('(', '').replace(' ',''))
#     y = int(str(y).replace(')', '').replace(' ',''))
#     pyautogui.click(x, y, button='left', clicks=1, interval=3)
#
#     pyautogui.click(1521, 849, button='left', clicks=1, interval=3)
#     pyautogui.click(1458, 636, button='left', clicks=1, interval=3)
#     pyautogui.click(1448, 249, button='left', clicks=1, interval=3)
#     pyautogui.click(1481, 807, button='left', clicks=1, interval=3)
#
#     while True:
#
#         time.sleep(3)
#         # 화면 캡처
#         monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}  # 캡처할 화면의 크기와 위치를 지정
#         with mss.mss() as sct:
#             image = np.array(sct.grab(monitor))
#         # 픽셀 값 가져오기
#         pixel_value = image[357, 1825]  # y , x
#         print(pixel_value)
#         val = str(pixel_value) not in '[121 163  55 255][ 47  47 179 255][105 171 208 255]'
#         if val:
#             break
###############################
