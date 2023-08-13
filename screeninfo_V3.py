# 바이킹 라이즈의 채집
# 로직 : 파견나간 영웅이 3/3이면 10분마다. 돌아온 영웅이 있는지 체크한다.
# 파견에서 돌아온 영웅이 있으면, 돋보기로 눌러서,
import time
import pyautogui
import random
import datetime as dt
import pytesseract
import cv2

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True  # False # True

def move_by_image(image, i):  #담벼락 따라 이동
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

def print_timestamp(msg):
    # print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(dt.datetime.now().strftime("%I:%M:%S"), msg)

def move_leftright(from_x, to_x, y, speed):
    pyautogui.moveTo(from_x, y)  # 찾은 자원 까지는 스킵 한다.
    pyautogui.dragTo(to_x, y, speed) # 0.2 초 짧은 시간 이동

def move_down(x, from_y, to_y, speed):
    pyautogui.click(1,random.choice([500, 1000, 1500]))   # 뻘짓해주고.
    pyautogui.moveTo(x, from_y)
    pyautogui.dragTo(x, to_y, speed) # 0.2 초 짧은 시간 이동


def find_two(star):
    find_x = 0
    space_cnt = 1
    dalguji_yn = ""
    # 1. 2등급 자원 찾기(자신의 영역에서 찾는다)y
    cur_button = pyautogui.locateOnScreen("02_cj_ssj_two.png", confidence=0.8,
                                          region=(500, 500, 2560 - 1000, 1600 - 1000))

    if cur_button is not None:  # 레벨 2 자원을 찾았으면
        print_timestamp(' ' * space_cnt + '02_cj_ssj_two')
        x, y, w, h = cur_button
        find_x = x  # 건너 뛰려고
        pyautogui.click(cur_button)  # 해당 자원을 클릭 한다
        time.sleep(0.1)

        # 달구지 부족의 자원인지
        cur_button = pyautogui.locateOnScreen("04_cj_dgj.png", confidence=0.8, region=(500, 500, 2560 - 1, 1600 - 1))
        if cur_button is not None:
            dalguji_yn = "y"
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
        else:
            # 달구지 부족의 자원이 아님을 알린다.
            dalguji_yn = "n"

    pyautogui.click(1, random.choice([500, 1000, 1500]), clicks=1, interval=0.1)  # 뻘짓해주고.
    return star, find_x, dalguji_yn


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

# 5
def adjust():
    speed = 0.2
    by = random.choice([1, 2, 3])
    xx = 500
    yy = 500
    pyautogui.moveTo(xx, yy / 1)  # 현위치
    pyautogui.dragTo(xx, (yy - 50) / 1, speed)  # 0.2 초 짧은 시간 이동
    # print(' '*0, "좌우로 정렬")


# 4
def image_to_string():  # 숫자 읽기.

    time.sleep(0)

    # 오른쪽    모니터의    너비와    높이를    가져옵니다.
    right_monitor_width = pyautogui.size()[0]
    right_monitor_height = pyautogui.size()[1]
    # print(right_monitor_width)
    # print(right_monitor_height)
    # 오른쪽    모니터의    화면을    캡처합니다.
    screenshot_path = 'screenshot_xy.png'
    # 이미지 저장
    pyautogui.screenshot(screenshot_path, region=(right_monitor_width / 2.86, right_monitor_height / 15, 240, 50))
    screenshot_image = cv2.imread(screenshot_path)

    text_time = pytesseract.image_to_string(screenshot_image)

    return text_time

# 3
def get_current_xy():   # 현위치 구하기
    x = 0
    y = 0
    try:
        while True:
            try_cnt = 0
            txt = ['00:00:02']

            text_time = image_to_string()  # 이미지에서 시간을 구해낸다.
            text_time = text_time.split('\n')
            x = int(text_time[0][3:6])
            y = int(text_time[0][10:15])

            # coordinate1 = (558, 1237)
            # coordinate2 = (696, 1178) # 3개 착기
            if x >= 500 and x <= 704 and y >= 1100 and y <= 1500:
                # print("현위치(정상)----------------->", str(x), str(y))
                break
            else:
                print(' ' * 10, "현위치(이상)----------------->", str(x), str(y))
                pyautogui.click(1, random.choice([500, 1000, 1500]), clicks=1, interval=1)  # 뻘짓해주고.
                adjust()
                time.sleep(2)
            # print('curr=',str(x), str(y))

        return x, y # 현위치를 반환 한다.

    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception as e:
        # print(e)
        # 예외가 발생한 경우 실행할 코드
        pyautogui.click(1, random.choice([500, 1000, 1500]))  # 뻘짓해주고.
        adjust()
        # print(' ' * 10, '현위치 반복으로 회피 기동 함.(밑으로 조금 이동)')
        return None, None


# 2
def move_to_target_coordinate(tx, ty, star_cnt):
    dx = 0
    dy = 0
    speed = 0.2
    prev_xx = 0
    prev_yy = 0
    i = 0
    # print('----> target=',str(tx),str(ty))
    # move_xy(tx, ty)

    while True:
        # 문자인식 : 현위치(최 상단 숫자 인식, xx, yy)
        xx, yy = get_current_xy()
        if prev_xx == 0:  # 처음엔 현재 위치를 저장
            prev_xx = xx
            prev_yy = yy
        if prev_xx == xx and prev_yy == yy:  # 이후엔 현위치가 동일하면 문제가 있는 것이므로, 회피..
            pyautogui.click(1, random.choice([500, 1000, 1500]), clicks=1, interval=1)  # 뻘짓해주고.
            adjust()
            # print(' ' * 10,  '현위치 반복으로 회피 기동 함.(밑으로 조금 이동)')
        else:
            prev_xx = xx  # 이전 위치 저장.
            prev_yy = yy

        # 현위치 잘 인식 되었으면
        if xx is not None and yy is not None:
            if abs(xx - tx) <= 3 and abs(yy - ty) <= 3:  # 오차 범위가 3 이내이면
                i = i + 1
                # print('근접', str((abs(xx - tx) + abs(yy - ty)) / 2) )
                time.sleep(0.2)
                # 2레벨의 자원지점이 있으면 북마크를 한다.
                star_cnt, find_x, dalguji_yn = find_two(star_cnt)
                '''
                if find_x != 0:  # 2레벨의 자원지점을 찾았으면
                    if dalguji_yn == "y":  # 달구지부족이면
                        move_find_skip(find_x)
                    else:
                        move_down(x, y, y - 200 / 1, 0.2)
                else:
                    move_leftright(x * 4, x, y, 1.0 + (x * 4) / 1000)  # 못찾으면 무조건 우측으로 이동 500픽셀씩...
                '''
                # print_timestamp(dalguji_yn + ' 있나?' + "{:>3}".format(i) + '  ' * 1 + '있네 : ' + str(star_cnt))
                print(' '*6, '자원?' + '' + dalguji_yn )  # + ' ' + '            ' + str(xx) + ', ' + str(yy))

                break
            else:
                # print('---> target=', str(tx), str(ty))
                dx = int(tx) - xx
                dy = int(ty) - yy
                print(' ' * 4 , '가까이 가자 =', str(dx), str(dy))

                by = random.choice([1,2,3])
                pyautogui.moveTo(xx, yy / by)  # 현위치
                # print('moveTo=', str(xx), str(yy / by))

                pyautogui.dragTo(xx - dx  * 100, (yy / by) + dy * 100, speed)  # 0.2 초 짧은 시간 이동
                # print('dragTo=', str(xx - dx  * 100), str((yy / by)+ dy * 100))

                pyautogui.click(1, random.choice([500, 1000, 1500]))  # 뻘짓해주고.
                # pyautogui.scroll(-1)
            time.sleep(0.9)
        else:
            print('' * 8, '에구 숫자 인식이 안되었네. 다시 문자인식 시도함.')
            time.sleep(3)


# 22
def move_xy(go_x, go_y, skip_yn):
    space_cnt = 2
    x = 0
    y = 0
    w = 0
    h = 0
    cur_button = pyautogui.locateOnScreen("02_cj_ssj_star.png", confidence=0.8,
                                          region=(500, 0, 300, 300))

    if cur_button is not None:  # 찾았으면
        # print_timestamp(' ' * space_cnt + '02_cj_ssj_star')
        x, y, w, h = cur_button
        # print(str(x), str(y))
        pyautogui.click(x + 100, y, clicks=1, interval=0.01)  #48 클릭 한다
        # time.sleep(0.1)
        pyautogui.click(x + 300, y + 500, clicks=1, interval=0.01)  # X 클릭
        # time.sleep(0.1)
        for n in str(go_x):
            # print(x)
            if n == '0':
                pyautogui.click(x + 300, y + 1050)  # 0 클릭 한다
            if n == '1':
                pyautogui.click(x + 300      , y + 950)  # 1 클릭 한다
            if n == '2':
                pyautogui.click(x + 300 + 200, y + 950)  # 2 클릭 한다
            if n == '3':
                pyautogui.click(x + 300 + 400, y + 950)  # 3 클릭 한다
            if n == '4':
                pyautogui.click(x + 300      , y + 850)  # 4 클릭 한다
            if n == '5':
                pyautogui.click(x + 300 + 200, y + 850)  # 5 클릭 한다
            if n == '6':
                pyautogui.click(x + 300 + 400, y + 850)  # 6 클릭 한다
            if n == '7':
                pyautogui.click(x + 300      , y + 750)  # 7 클릭 한다
            if n == '8':
                pyautogui.click(x + 300 + 200, y + 750)  # 8 클릭 한다
            if n == '9':
                pyautogui.click(x + 300 + 400, y + 750)  # 9 클릭 한다

        if skip_yn == 'n':
            pyautogui.click(x + 700, y + 500, clicks=2, interval=0.1)  # Y 클릭
            # ime.sleep(0.1)
            for n in str(go_y):
                # print(x)
                if n == '0':
                    pyautogui.click(x + 700, y + 1050)  # 0 클릭 한다
                if n == '1':
                    pyautogui.click(x + 700      , y + 950)  # 1 클릭 한다
                if n == '2':
                    pyautogui.click(x + 700 + 200, y + 950)  # 2 클릭 한다
                if n == '3':
                    pyautogui.click(x + 700 + 400, y + 950)  # 3 클릭 한다
                if n == '4':
                    pyautogui.click(x + 700      , y + 850)  # 4 클릭 한다
                if n == '5':
                    pyautogui.click(x + 700 + 200, y + 850)  # 5 클릭 한다
                if n == '6':
                    pyautogui.click(x + 700 + 400, y + 850)  # 6 클릭 한다
                if n == '7':
                    pyautogui.click(x + 700      , y + 750)  # 7 클릭 한다
                if n == '8':
                    pyautogui.click(x + 700 + 200, y + 750)  # 8 클릭 한다
                if n == '9':
                    pyautogui.click(x + 700 + 400, y + 750)  # 9 클릭 한다
            # time.sleep(1)
        pyautogui.click(x + 1100, y + 500, clicks=2, interval=0.1)  # 이동하기 클릭
        # time.sleep(0.1)
    # time.sleep(0.1)

# 2 - v2
def move_to_target_coordinate_v2(tx, ty, star_cnt, skip_yn):
    move_xy(tx, ty, skip_yn)
    # 2레벨의 자원지점이 있으면 북마크를 한다.
    star_cnt, find_x, dalguji_yn = find_two(star_cnt)
    print(' ' * len('     다음 좌표 (568, 1238) 3 1  3 of 540'), '북마킹성공 ?' + ' ' + dalguji_yn) # + ' ' + '            ' + str(tx) + ', ' + str(ty))


def is_inside_polygon(polygon, x, y):
    n = len(polygon)
    odd_nodes = False
    j = n - 1

    for i in range(n):
        if (polygon[i][1] < y and polygon[j][1] >= y) or (polygon[j][1] < y and polygon[i][1] >= y):
            if polygon[i][0] + (y - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) * (polygon[j][0] - polygon[i][0]) < x:
                odd_nodes = not odd_nodes
        j = i

    return odd_nodes

# 1
def clean_area(coordinates, coord1, coord2, star_cnt, start_num): # 한 영역 씩 이동 하면서 등록 한다.
    # 좌표가 주어진 순서와 관계없이 직사각형의 네 모서리 좌표를 계산
    # min_x = min(coord1[0], coord2[0])
    # max_x = max(coord1[0], coord2[0])
    # min_y = min(coord1[1], coord2[1])
    # max_y = max(coord1[1], coord2[1])
    min_x = min(coordinates, key=lambda c: c[0])[0]
    max_x = max(coordinates, key=lambda c: c[0])[0]
    min_y = min(coordinates, key=lambda c: c[1])[1]
    max_y = max(coordinates, key=lambda c: c[1])[1]
    y_cnt = 0
    x_cnt = 0
    xy_cnt = 0
    d = 3 # 밑으로  2
    r = 5 # 오른쪽을 4
    prev_y = 0
    ret_num = start_num

    coord_cnt = int((max_y + 1 - min_y) / d) * int(( max_x + 1 - min_x) / r)
    for y in range(max_y + 1, min_y, -1 * d): # 밑으로 -2씩
        y_cnt = y_cnt + 1
        x_cnt= 0
        for x in range(min_x, max_x + 1, r): # 오른쪽으로 4씩.
            x_cnt = x_cnt + 1
            xy_cnt = xy_cnt + 1
            ret_num = xy_cnt
            # print(str(ret_num),'x')

            # 파일을 쓰기 모드로 열기
            with open("next_num.txt", "w") as file:
                file.write(str(xy_cnt))

            print(' '*2, f"다음 좌표 ({x}, {y})", str(x_cnt), str(y_cnt), ' ' + str(xy_cnt) + ' of ' + str(coord_cnt))

            if is_inside_polygon(coordinates, x, y):
                if xy_cnt >= start_num:  # 이전 위치이후인지. (다각형안의 영역이면서)
                    ret_num = num_bookmarking(start_num)
                    # print(str(ret_num), str(start_num), 'y')

                    if ret_num != start_num: # 4/4을 발견 했으므로, 북마킹을 시작하자.
                        if prev_y == 0:
                            prev_y = y
                            move_to_target_coordinate_v2(int(x), int(y), star_cnt, 'n')
                        else:
                            if y == prev_y:
                                move_to_target_coordinate_v2(int(x), int(y), star_cnt, random.choice(['y','n']) )
                            else:
                                prev_y = y
                                move_to_target_coordinate_v2(int(x), int(y), star_cnt, 'n')
                    else:
                        # print(str(ret_num), 'z')

                        return ret_num # 북마킹을 중단하자. 중단번호 넘기기.

    # print(str(ret_num), 'x, y 전부 돈 후.')
    return ret_num

def clean_area_no_use(coordinates, coord1, coord2, star_cnt, start_num):
    min_x = min(coordinates, key=lambda c: c[0])[0]
    max_x = max(coordinates, key=lambda c: c[0])[0]
    min_y = min(coordinates, key=lambda c: c[1])[1]
    max_y = max(coordinates, key=lambda c: c[1])[1]
    y_cnt = 0
    x_cnt = 0
    xy_cnt = 0
    d = 3  # 밑으로  2
    r = 5  # 오른쪽을 4
    prev_y = 0

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if is_inside_polygon(coordinates, x, y):
                print(f"Cleaning coordinate ({x}, {y})")

# 북마킹 가능 여부 : 북마킹 불가능 상태 이면 입력된 번호 그대로, 가능하다면 + 1 : 가능 상태라 함은 전부 출동...그리고...북마크 쓸만한 거 1개 남음.
def num_bookmarking_nouse(num):
    found_button = pyautogui.locateOnScreen('01_cj_44' + ".png", confidence=0.9, region=(0, 0, 2560 - 10, 1600 - 10))
    if found_button is not None:
        print('01_cj_44')
        x, y, w, h = found_button
        found_button = pyautogui.locateOnScreen('02_cj_ssj_star' + ".png", confidence=0.9, region=(0, 0, 2560 - 10, 1600 - 10))
        if found_button is not None:
            print('02_cj_ssj_star')
            x, y, w, h = found_button
            pyautogui.click(x, y, button='left', clicks=1, interval=0.1)  # 자원 버튼 클릭
            time.sleep(0.2)
            found_button = pyautogui.locateOnScreen('02_cj_ssj_star_redcross' + ".png", confidence=0.9, region=(0, 0, 2560 - 10, 1600 - 10))
            if found_button is not None:
                print('02_cj_ssj_star_redcross')
                x, y, w, h = found_button
                pyautogui.click(x, y, button='left', clicks=1, interval=0.1)  # 자원 버튼 클릭

                found_button = pyautogui.locateOnScreen('02_cj_cross' + ".png", confidence=0.9, region=(0, 0, 2560 - 10, 1600 - 10))
                if found_button is not None:
                    print('02_cj_cross')
                    x, y, w, h = found_button
                    pyautogui.click(x, y, button='left', clicks=1, interval=0.1)  # 자원 버튼 클릭

                    num = num + 1
                    return num
    return num

def num_bookmarking(num):
    found_button = pyautogui.locateOnScreen('01_cj_44' + ".png", confidence=0.9, region=(0, 0, 2560 - 10, 1600 - 10))
    if found_button is not None:
        print_timestamp('01_cj_44')
        num = num + 1
        return num

    return num

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
start_num = 1
last_num = 609
# 사용 예시
# coordinate1 = (558, 1237)
coordinate1 = (558, 1237)
coordinate2 = (696, 1178) # 3개 착기
# ------------------------------------------------------------------------ # 시작 here
coordinates = [(560, 1239),    (560, 1227),    (595, 1227),    (595, 1219),    (603, 1219),    (604, 1215),    (611, 1215),    (612, 1203),    (623, 1203),    (623, 1211),    (627, 1211),    (627, 1193),    (612, 1191),    (608, 1187),    (608, 1179),    (631, 1183),    (647, 1183),    (647, 1191),    (659, 1191),    (659, 1195),    (671, 1195),    (672, 1199),    (695, 1199),    (703, 1203),    (704, 1212),    (672, 1212),    (672, 1208),    (668, 1208),    (668, 1232),    (656, 1232),    (656, 1208),    (660, 1208),    (660, 1204),    (640, 1204),    (640, 1212),    (636, 1212),    (636, 1220),    (648, 1220),    (648, 1232),    (636, 1232),    (636, 1224),    (624, 1223),    (624, 1216),    (616, 1216),    (616, 1227),    (608, 1228),    (608, 1231),    (596, 1232),    (596, 1239)]
while True:
    # 파일을 읽기 모드로 열기
    with open("next_num.txt", "r") as file:
        start_num = int(file.read())
    if start_num == last_num:
        start_num = 1
    print(str(start_num))
    ret_num = num_bookmarking(start_num)
    if ret_num != start_num:
        time.sleep(6)
        ret_num = clean_area(coordinates, coordinate1, coordinate2, star_cnt, start_num)

        if ret_num == last_num:
            start_num = 1
        else:
            start_num = ret_num
    print('x')
    time.sleep(6)



'''
# 좌표 찍기. 영토.
from pynput.mouse import Listener, Button

def on_double_click(x, y, button, pressed):
    if pressed and button == Button.right:
        xxx, yyy = get_current_xy()
        print("({}, {}),".format(xxx, yyy))

def main():
    with Listener(on_click=on_double_click) as listener:
        listener.join()

if __name__ == "__main__":
    main()
'''