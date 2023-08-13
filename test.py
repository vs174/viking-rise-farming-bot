import pyautogui
import time
import datetime as dt

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

def clean_area(coordinates):
    min_x = min(coordinates, key=lambda c: c[0])[0]
    max_x = max(coordinates, key=lambda c: c[0])[0]
    min_y = min(coordinates, key=lambda c: c[1])[1]
    max_y = max(coordinates, key=lambda c: c[1])[1]

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if is_inside_polygon(coordinates, x, y):
                print(f"Cleaning coordinate ({x}, {y})")


# coordinates = [(0, 4), (0, 1), (1, 1), (1, 0),(5,0),(5,4),(4,4),(4,2),(2,2),(2,4)]
# clean_area(coordinates)


def on_double_click(x, y):
  print("Double clicked at ({}, {})".format(x, y))

def on_mouse_double_click(x, y, button, pressed):
  print("Mouse double clicked at ({}, {})".format(x, y))


from pynput.mouse import Listener, Button

def on_double_click(x, y, button, pressed):
    if pressed and button == Button.right:
        print("Double clicked at ({}, {})".format(x, y))


# 좌표 찍기. 영토.
from pynput.mouse import Listener, Button

def on_double_click(x, y, button, pressed):
    if pressed and button == Button.right:
        xxx, yyy = get_current_xy()
        print("({}, {}),".format(xxx, yyy))

def main():
    with Listener(on_click=on_double_click) as listener:
        listener.join()

# if __name__ == "__main__":
#     main()

def num_bookmarking(num):
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

# start main
print(str(num_bookmarking(1)))


'''
import pyautogui
import time
import datetime as dt

def print_timestamp(msg):
    # print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(dt.datetime.now().strftime("%I:%M:%S"), msg)




def move_xy(go_x, go_y):
    space_cnt = 2
    x = 0
    y = 0
    w = 0
    h = 0
    cur_button = pyautogui.locateOnScreen("02_cj_ssj_star.png", confidence=0.8,
                                          region=(500, 0, 300, 300))

    if cur_button is not None:  # 찾았으면
        print_timestamp(' ' * space_cnt + '02_cj_ssj_star')
        x, y, w, h = cur_button
        print(str(x), str(y))
        pyautogui.click(x + 100, y, clicks=1, interval=0.2)  #48 클릭 한다
        time.sleep(0.5)
        pyautogui.click(x + 300, y + 500, clicks=1, interval=0.2)  # X 클릭
        time.sleep(0.5)
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

        pyautogui.click(x + 700, y + 500, clicks=2, interval=0.2)  # Y 클릭
        time.sleep(0.5)
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
        pyautogui.click(x + 1100, y + 500, clicks=2, interval=0.2)  # 이동하기 클릭
        time.sleep(0.1)
    time.sleep(0.1)

coordinates = [(560, 1239),
(560, 1227),
(595, 1227),
(595, 1219),
(603, 1219),
(604, 1215),
(611, 1215),
(612, 1203),
(623, 1203),
(623, 1211),
(627, 1211),
(627, 1193),
(612, 1191),
(608, 1187),
(608, 1179),
(631, 1183),
(647, 1183),
(647, 1191),
(659, 1191),
(659, 1195),
(671, 1195),
(672, 1199),
(695, 1199),
(703, 1203),
(704, 1212),
(672, 1212),
(672, 1208),
(668, 1208),
(668, 1232),
(656, 1232),
(656, 1208),
(660, 1208),
(660, 1204),
(640, 1204),
(640, 1212),
(636, 1212),
(636, 1220),
(648, 1220),
(648, 1232)]

move_xy(coordinates)
'''