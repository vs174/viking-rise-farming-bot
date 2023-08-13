# 바이킹 라이즈의 채집
# 로직 : 파견나간 영웅이 3/3이면 10분마다. 돌아온 영웅이 있는지 체크한다.
# 파견에서 돌아온 영웅이 있으면, 돋보기로 눌러서,
import time
import pyautogui
import random
import datetime as dt
import sys
import cv2

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

def print_timestamp(msg):
    # print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(dt.datetime.now().strftime("%I:%M:%S"), msg)

# 마우스 커서를 (100, 100) 위치로 이동합니다.
x = 500
y = 500
x_step = 500
y_step = 500
w = 0
h = 0
find_x = 2560 * 4 / 5
pyautogui.click(x, y, button='left', clicks=1, interval=0.1)
prev_button = ""

same_button_cnt = 0
r_cnt = 0
down_y = 500
star_cnt = 0
max_x = 0

while True:
    cur_button = ""
    # center = pyautogui.center()
    cur_button = pyautogui.locateOnScreen("05_cj_hour6.png", confidence=0.9, region=(500, 500, 2560 - 1000, 1600 - 1000))
    # 버튼 주위에 선 그리기
    # pyautogui.dragTo(cur_button, cur_button + (50, 50), duration=2)

    print_timestamp('a')
    if cur_button is not None:
        pyautogui.click(1, random.choice([500, 1000]))
        pyautogui.moveTo(1, 500)  # 없으면 확 넘어간다.
        pyautogui.dragTo(random.choice([2560, 2570, 2580]) * 4 / 5, 500, 1)  # 100: 덜 보내야 한다.

        print('hit')
        break
        x, y, w, h = cur_button
        find_x = x
        pyautogui.click(cur_button)
    time.sleep(0.9)


    #     cur_button = pyautogui.locateOnScreen("04_cj_dgj.png", confidence=0.7, region=(500, 500, 2560 - 1 , 1600 - 1))
    #     print_timestamp(' b')
    #     if cur_button is not None:
    #         x, y, w, h = cur_button
    #         pyautogui.click(cur_button)
    #
    #         cur_button = pyautogui.locateOnScreen("04_cj_flag.png", confidence=0.7, region=(1, 1, 2560 - 1 , 800))
    #         print_timestamp('  c')
    #         if cur_button is not None:
    #             x, y, w, h = cur_button
    #             pyautogui.click(cur_button)
    #
    #             cur_button = pyautogui.locateOnScreen("04_cj_flag_gaein.png", confidence=0.7, region=(1, 1, 2560 - 1, 800))
    #             print_timestamp('    d')
    #             if cur_button is not None:
    #                 x, y, w, h = cur_button
    #                 pyautogui.click(cur_button)
    #
    #                 cur_button = pyautogui.locateOnScreen("04_cj_confirm.png", confidence=0.7,  region=(1, 1, 2560 - 1, 1600 - 1))
    #                 print_timestamp('     e')
    #                 if cur_button is not None:
    #                     x, y, w, h = cur_button
    #                     pyautogui.click(cur_button)
    #                     star_cnt = star_cnt + 1
    #
    # # 직전 검색한 위치까지는 통과하도록 한다. #
    # print_timestamp('stared : ' + str(star_cnt))
    # time.sleep(0.1)
    # pyautogui.click(1, random.choice([500, 1000]))
    # pyautogui.moveTo(find_x, 500) # 없으면 확 넘어간다.
    # time.sleep(0.1)
    # #  print('y')
    # pyautogui.dragTo(random.choice([2560, 2570, 2580]) * 1 / 10, 500, 2) # 100: 덜 보내야 한다.
    # find_x = 2560 * 4 / 5
    # r_cnt = r_cnt + 1
    # print_timestamp(r_cnt)
    # # print('-', r_cnt)
    # if r_cnt >= 30: # 오른쪽으로 30회 이동했으면, 원위치 하기 위하여. 아래 실행.
    #     r_cnt = 0
    #     my_cnt = 0
    #     while True: # 왼쪽으로  30회 이동후 아래로 1회 내려가고, 브레이크.
    #         pyautogui.click(1, random.choice([500, 1000]))
    #         pyautogui.moveTo(1, 500)  # 없으면 확 넘어간다.
    #         pyautogui.dragTo(random.choice([2560, 2570, 2580]) * 4 / 5, 500, 1)  # 100: 덜 보내야 한다.
    #         my_cnt = my_cnt + 1
    #         print_timestamp(my_cnt * 1)
    #         if my_cnt >= 24: # 밑으로
    #             pyautogui.click(1, random.choice([500, 1000]))
    #             pyautogui.moveTo(1, 1000)  # 없으면 확 넘어간다.
    #             pyautogui.dragTo(1, 400, 1)  # 100: 덜 보내야 한다.
    #             break
    #
    # time.sleep(1)



    ############################################################

    # if cur_button is not None:
    #     x, y, w, h = cur_button
    #     if x >= 700: # 부족 영토의 오른쪽 끝 . 상수값. 700
    #         x = 560 # 맨 왼쪽으로 온다.부족 영토의 왼쪽 끝값 . 상수값 560
    #         y = y + 600 # 600정도 아래로 내려 준다.




    # xx = 500
    # yy = 500
    # x_step = 10
    # y_step = 0
    # xx = xx + x_step
    # yy = yy + y_step
    # print('x')
    #
    # if cur_button is None:
    #     print('없음')
    #     pyautogui.click(1, random.choice([400,600,800,1000]))
    #     pyautogui.moveTo(2560 / 2, 500) # 없으면 확 넘어간다.
    #     time.sleep(3)
    #     print('y')
    #     pyautogui.dragTo(1, 500, 1)
    #     print('z')
    # else: # 있으면 확지나가야지.
    #     print('있음')
    #     pyautogui.click(1, random.choice([400,600,800,1000]))
    #     pyautogui.moveTo(x / 2 , 500)
    #     time.sleep(3)
    #     print('yy')
    #     pyautogui.dragTo(1, 500, 1)
    #     print('zz')
    # # if cur_button is None:
    #     # 마우스를 (100, 100) 위치로 이동합니다.
    #
    #
    #     # 마우스를 (200, 200) 위치로 드래그합니다.
    #     # pyautogui.dragTo(400, 400, 1000)
    #     # print('-------------')
    #
    # button_x  =x
    # button_y = y
    #
    # # 버튼 주위에 선 그리기
    # # if cur_button is not None:
    # #     pyautogui.dragTo(100, 100, 10)
    #     # pyautogui.dragTo(cur_button, cur_button + (50, 50), duration=2)
    # #    print('--------------------------------------')
    # time.sleep(3)
    # nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
    # position = pyautogui.position()
    #
    # print(position)
    #
    # time.sleep(0.1)
    # pyautogui.scroll(100)
    # time.sleep(0.1)
    #



    # if prev_button == "":
    #     prev_button = cur_button
    #     same_button_cnt = same_button_cnt + 1
    # elif prev_button == cur_button:  # 무한 루프 조짐.
    #     same_button_cnt = same_button_cnt + 1
    # else:
    #     prev_button = cur_button
    #     same_button_cnt = 1
    # # print(str(same_button_cnt), prev_button, cur_button)
    #
    # if same_button_cnt == 10:
    #     print("무한루프 시간")
    #     pyautogui.scroll(100)
    #
    #     cur_button_loop = pyautogui.locateOnScreen("02_cj_cross.png", confidence=0.7, region=(0, 0, 2560, 1600))
    #     pyautogui.click(cur_button_loop)
    #     pyautogui.scroll(100)
    #
    #     offset_y = random.choice([200, 400, 600, 800, 1000, 1200, 1400, 1600])
    #     pyautogui.click(x=2, y=offset_y, button='left', clicks=1, interval=0.1)  # 탈출
    #     pyautogui.scroll(100)
    #
    #     prev_button = ""
    #     same_button_cnt = 0
    # 3회 이상 동일한 메시지가 나오면 무언가 처리한다.
