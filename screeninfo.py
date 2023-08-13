# 바이킹 라이즈의 채집
# 로직 : 파견나간 영웅이 3/3이면 10분마다. 돌아온 영웅이 있는지 체크한다.
# 파견에서 돌아온 영웅이 있으면, 돋보기로 눌러서,
import time
import pyautogui
import random
import datetime as dt

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

def print_timestamp(msg):
    # print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(dt.datetime.now().strftime("%I:%M:%S"), msg)

def move_leftright(from_x, to_x, y, speed):
    pyautogui.moveTo(from_x, y)  # 찾은 자원 까지는 스킵 한다.
    pyautogui.dragTo(to_x, y, speed) # 0.2 초 짧은 시간 이동

def move_down(x, from_y, to_y, speed):
    pyautogui.moveTo(x, from_y)  # 찾은 자원 까지는 스킵 한다.
    pyautogui.dragTo(x, to_y, speed) # 0.2 초 짧은 시간 이동

def on_mouse_move(x, y, delta_x, delta_y, button):
    if delta_y > 100:
        # 마우스가 위로 100px 이상 움직이면 프로그램을 종료한다.
        sys.exit()

def find_two(star):
    find_x = 0
    space_cnt = 1
    # 1. 2등급 자원 찾기(속알맹이 영역에서 찾는다)
    cur_button = pyautogui.locateOnScreen("02_cj_ssj_two.png", confidence=0.8,
                                          region=(500, 500, 2560 - 1000, 1600 - 1000))

    if cur_button is not None:  # 자원을 찾았으면
        print_timestamp(' ' * space_cnt + '02_cj_ssj_two')
        x, y, w, h = cur_button
        find_x = x  # 건너 뛰려고
        pyautogui.click(cur_button)  # 해당 자원을 클릭 한다
        time.sleep(0.1)

        # 달구지 부족의 자원인지
        cur_button = pyautogui.locateOnScreen("04_cj_dgj.png", confidence=0.8, region=(500, 500, 2560 - 1, 1600 - 1))
        if cur_button is not None:
            print_timestamp(' ' * space_cnt + '04_cj_dgj')
            x, y, w, h = cur_button
            pyautogui.click(cur_button)

            # 플래그 클릭
            cur_button = pyautogui.locateOnScreen("04_cj_flag.png", confidence=0.8, region=(1, 1, 2560 - 1, 800))
            if cur_button is not None:
                print_timestamp(' ' * space_cnt + '04_cj_flag')
                x, y, w, h = cur_button
                pyautogui.click(cur_button)

                # 개인 클릭
                cur_button = pyautogui.locateOnScreen("04_cj_flag_gaein.png", confidence=0.8,
                                                      region=(1, 1, 2560 - 1, 800))
                if cur_button is not None:
                    print_timestamp(' ' * space_cnt + '04_cj_flag_gaein')
                    x, y, w, h = cur_button
                    pyautogui.click(cur_button)

                    # 확인 클릭 : 북마킹이 등록 된다.
                    cur_button = pyautogui.locateOnScreen("04_cj_confirm.png", confidence=0.8,
                                                          region=(1, 1, 2560 - 1, 1600 - 1))
                    if cur_button is not None:
                        print_timestamp(' ' * space_cnt + '04_cj_confirm')
                        x, y, w, h = cur_button
                        pyautogui.click(cur_button)
                        star = star + 1  # 북마크 등록 완료 개수
    return star, find_x


def move_find_skip(find_x):
    pyautogui.moveTo(find_x, 500)  # 찾은 자원 까지는 스킵 한다.
    print(str(find_x) + ':')
    pyautogui.dragTo(random.choice([2200, 2300, 2400]) * 1 / 5, 500, 0.2 + find_x / 1000) # 2.2: 정확히 보내기 위해 시간 충분히. 준다.
    pyautogui.click(1, random.choice([400, 800]))  # 회피 기동

def check_right_end_go_to_left_end(i):
    space_cnt = 1
    right_find = "no"
    left_find = "no"
    cur_button = pyautogui.locateOnScreen("05_cj_hour77" + ".png", confidence=0.8,
                                          region=(500, 500, 2560 - 500 * 2, 1600 - 500 * 2))
    if cur_button is not None:  # 찾았으면
        right_find = "yes"
    else:
        cur_button = pyautogui.locateOnScreen("05_cj_hour66" + ".png", confidence=0.8,
                                              region=(500, 500, 2560 - 500 * 2, 1600 - 500 * 2))
        if cur_button is not None:  # 찾았으면
            right_find = "yes"
        else:
            cur_button = pyautogui.locateOnScreen("05_cj_hour55" + ".png", confidence=0.8,
                                                  region=(500, 500, 2560 - 500 * 2, 1600 - 500 * 2))
            if cur_button is not None:  # 찾았으면
                right_find = "yes"

    if right_find == "yes":
        print_timestamp(' ' * space_cnt + 'right_find')
        move_down(1, 500, 500 - 250 , 1.0)
        while True:
            cur_button = pyautogui.locateOnScreen("05_cj_hour1111" + ".png", confidence=0.8,
                                                  region=(500, 500, 2560 - 500 * 2, 1600 - 500 * 2))
            if cur_button is not None:  # 자원을 찾았으면
                print_timestamp(' ' * space_cnt + '1 left_find')
                left_find = "yes"
            else:
                cur_button = pyautogui.locateOnScreen("05_cj_hour1212" + ".png", confidence=0.8,
                                                      region=(500, 500, 2560 - 500 * 2, 1600 - 500 * 2))
                if cur_button is not None:  # 자원을 찾았으면
                    print_timestamp(' ' * space_cnt + '2 left_find')
                    left_find = "yes"
                else:
                    cur_button = pyautogui.locateOnScreen("05_cj_hour1313" + ".png", confidence=0.8,
                                                          region=(500, 500, 2560 - 500 * 2, 1600 - 500 * 2))
                    if cur_button is not None:  # 자원을 찾았으면
                        print_timestamp(' ' * space_cnt + '3 left_find')
                        left_find = "yes"

            if left_find == "yes":
                print_timestamp(' ' * space_cnt + 'left_find')
                break
            else:
                x = 2500 * 4 / 5
                y = 500
                move_leftright(499, x, y, 1.0)  # 왼쪽으로 갈때는 막 건너 뛴다.


def move_by_image(image, i):
    cur_button = pyautogui.locateOnScreen(image + ".png", confidence=0.90, region=(500, 500, 2560 - 500 * 2, 1600 - 500 * 2))
    if cur_button is not None:  # 자원을 찾았으면
        pyautogui.click(cur_button)  # 해당 자원을 클릭 한다
        print_timestamp(' ' * 5 + "{:>5}".format(i) + ' ' * 2 + image)
        x, y, w, h = cur_button
        find_x = x
        if image == "05_cj_hour77":
            move_down(x, y, y - 200 / 1, 0.2)
            move_leftright(x - 200 / 2, x, y, 0.2)
            # move_to_left(x, y)

        if image == "05_cj_hour66":
            move_down(x, y, y - 200 / 1, 0.2)
            # move_to_left(x, y)

        if image == "05_cj_hour55":
            move_down(x, y, y - 200 / 1, 0.2)
            move_leftright(x, x - 200 / 2, y, 0.2)
            # move_to_left(x, y)

        if image == "05_cj_hour33":
            move_leftright(x, x - 200 / 1, y, 0.2)

        pyautogui.click(1, random.choice([400, 800]))  # 회피 기동

        # pyautogui.click(cur_button)  # 해당 자원을 클릭 한다
        time.sleep(0.1)



# 마우스 커서를 (100, 100) 위치로 이동합니다.
x = 500
y = 500
x_step = 500
y_step = 500
w = 0
h = 0
find_x = 2560 / 1000
prev_button = ""
same_button_cnt = 0
r_cnt = 0
down_y = 500
star_cnt = 0
i = 0
direction = 'right'
while True:
    i = i + 1

    # 2레벨의 자원지점이 있으면 북마크를 한다.
    star_cnt, find_x = find_two(star_cnt)
    if find_x != 0: # 찾았으면 스킵하려고.
        move_find_skip(find_x)
    else:
        move_leftright(x, x - 499, y, 1) # 못찾으면 무조건 우측으로 이동 500픽셀씩...

    check_right_end_go_to_left_end(i)

    print_timestamp(' 찾기시도 :' + "{:>3}".format(i) + ' ' * 4 + '북마킹 : ' + str(star_cnt))
    # pyautogui.click(500, 500)  # 시작점
    time.sleep(3.1)

    # 에고--------------- 끝.

    # start here ------------------------------------------------------------------here
    # break
    #
    # 1. 2등급 자원 찾기(속알맹이 영역에서 찾는다)
    # cur_button = pyautogui.locateOnScreen("02_cj_ssj_two.png", confidence=0.8, region=(500, 500, 2560 - 1000, 1600 - 1000))
    # print_timestamp('02_cj_ssj_two')
    # if cur_button is not None:  # 자원을 찾았으면
    #     x, y, w, h = cur_button
    #     find_x = x  # 건너 뛰려고
    #     pyautogui.click(cur_button)  # 해당 자원을 클릭 한다
    #     time.sleep(0.1)
    #
    #     # 달구지 부족의 자원인지
    #     cur_button = pyautogui.locateOnScreen("04_cj_dgj.png", confidence=0.8, region=(500, 500, 2560 - 1 , 1600 - 1))
    #     print_timestamp('04_cj_dgj')
    #     if cur_button is not None:
    #         x, y, w, h = cur_button
    #         pyautogui.click(cur_button)
    #
    #         # 플래그 클릭
    #         cur_button = pyautogui.locateOnScreen("04_cj_flag.png", confidence=0.8, region=(1, 1, 2560 - 1 , 800))
    #         print_timestamp('04_cj_flag')
    #         if cur_button is not None:
    #             x, y, w, h = cur_button
    #             pyautogui.click(cur_button)
    #
    #             # 개인 클릭
    #             cur_button = pyautogui.locateOnScreen("04_cj_flag_gaein.png", confidence=0.8, region=(1, 1, 2560 - 1, 800))
    #             print_timestamp('04_cj_flag_gaein')
    #             if cur_button is not None:
    #                 x, y, w, h = cur_button
    #                 pyautogui.click(cur_button)
    #
    #                 # 확인 클릭 : 북마킹이 등록 된다.
    #                 cur_button = pyautogui.locateOnScreen("04_cj_confirm.png", confidence=0.8,  region=(1, 1, 2560 - 1, 1600 - 1))
    #                 print_timestamp('04_cj_confirm')
    #                 if cur_button is not None:
    #                     x, y, w, h = cur_button
    #                     pyautogui.click(cur_button)
    #                     star_cnt = star_cnt + 1 # 북마크 등록 완료 개수

    # 2. 오른쪽으로 이동 시작.
    # print_timestamp('               북마킹 : ' + str(star_cnt))   # 북마킹 성공의 개수 표시
    # time.sleep(0.1)
    # pyautogui.click(1, random.choice([500, 1000]))
    # pyautogui.moveTo(find_x, 500) # 찾은 자원 까지는 스킵 한다.
    # pyautogui.dragTo(random.choice([2560, 2570, 2580]) * 1 / 10, 500, 0.2) # 100: 덜 보내야 한다.
    # find_x = 2560 * 4 / 5
    # r_cnt = r_cnt + 1
    # print_timestamp(r_cnt) # 오른쪽으로 이동한 횟수 : 최대 30회까지 간다. ---->
    #
    # if r_cnt >= 30: # 오른쪽으로 30회 이동했으면, 원위치 하기 위하여. 아래 실행.     V
    #     # 아래로 한줄 내려간다.
    #     pyautogui.click(1, random.choice([500, 1000]))
    #     pyautogui.moveTo(1, 1000)  # 아래 클릭.
    #     pyautogui.dragTo(1, 400, 0.2)  # 위로 드래그
    #
    #     r_cnt = 0
    #     my_cnt = 0
    #     while True: # 왼쪽으로  30회 이동 <-----
    #         pyautogui.click(1, random.choice([500, 1000]))
    #         pyautogui.moveTo(1, 500)  # 왼쪽 클릭
    #         pyautogui.dragTo(random.choice([2560, 2570, 2580]) * 4 / 5, 500, 0.2)  # 오른쪽으로 드래그
    #
    #         # 자원찾아, 북마킹하기.
    #         # 3. 2등급 자원 찾기(속알맹이 영역에서 찾는다)
    #         cur_button = pyautogui.locateOnScreen("02_cj_ssj_two.png", confidence=0.8,
    #                                               region=(500, 500, 2560 - 1000, 1600 - 1000))
    #         print_timestamp('자원')
    #         if cur_button is not None:  # 자원을 찾았으면
    #             x, y, w, h = cur_button
    #             find_x = x  # 건너 뛰려고
    #             pyautogui.click(cur_button)  # 해당 자원을 클릭 한다
    #             time.sleep(0.1)
    #
    #             # 달구지 부족의 자원인지
    #             cur_button = pyautogui.locateOnScreen("04_cj_dgj.png", confidence=0.8,
    #                                                   region=(500, 500, 2560 - 1, 1600 - 1))
    #             print_timestamp('자원-소속')
    #             if cur_button is not None:
    #                 x, y, w, h = cur_button
    #                 pyautogui.click(cur_button)
    #
    #                 # 플래그 클릭
    #                 cur_button = pyautogui.locateOnScreen("04_cj_flag.png", confidence=0.8,
    #                                                       region=(1, 1, 2560 - 1, 800))
    #                 print_timestamp('자원-소속-깃발')
    #                 if cur_button is not None:
    #                     x, y, w, h = cur_button
    #                     pyautogui.click(cur_button)
    #
    #                     # 개인 클릭
    #                     cur_button = pyautogui.locateOnScreen("04_cj_flag_gaein.png", confidence=0.8,
    #                                                           region=(1, 1, 2560 - 1, 800))
    #                     print_timestamp('자원-소속-깃발-개인')
    #                     if cur_button is not None:
    #                         x, y, w, h = cur_button
    #                         pyautogui.click(cur_button)
    #
    #                         # 확인 클릭 : 북마킹이 등록 된다.
    #                         cur_button = pyautogui.locateOnScreen("04_cj_confirm.png", confidence=0.8,
    #                                                               region=(1, 1, 2560 - 1, 1600 - 1))
    #                         print_timestamp('자원-소속-깃발-개인-확인')
    #                         if cur_button is not None:
    #                             x, y, w, h = cur_button
    #                             pyautogui.click(cur_button)
    #                             star_cnt = star_cnt + 1  # 북마크 등록 완료 개수
    #
    #         # 4. 30회 하고 나면 아래로 이동.
    #         my_cnt = my_cnt + 1
    #         print_timestamp(my_cnt * 1)
    #         if my_cnt >= 30: # 밑으로
    #             # 아래로 한줄
    #             pyautogui.click(1, random.choice([500, 1000]))
    #             pyautogui.moveTo(1, 1000)  # 아래 클릭.
    #             pyautogui.dragTo(1, 400, 0.2)  # 위로 드래그
    #             break
    # here ==============================================================================


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
    #     cur_button_loop = pyautogui.locateOnScreen("02_cj_cross.png", confidence=0.8, region=(0, 0, 2560, 1600))
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
