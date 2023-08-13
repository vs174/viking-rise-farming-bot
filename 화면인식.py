# 화면 인식 테스트 - 없어져도 됨.
# import time
import pyautogui
import cv2
import numpy as np
# from PIL import Image


def capture_and_recognize_image(template_image_path):
    # 화면 캡처
    screenshot = pyautogui.screenshot()

    # 이미지 저장
    screenshot_path = 'screenshot.png'
    screenshot.save(screenshot_path)

    # 템플릿 이미지 로드
    template_image = cv2.imread(template_image_path)
    template_image_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
    template_width, template_height = template_image_gray.shape[::-1]

    # 화면 캡처 이미지 로드
    screenshot_image = cv2.imread(screenshot_path)
    screenshot_image_gray = cv2.cvtColor(screenshot_image, cv2.COLOR_BGR2GRAY)

    # 이미지 매칭
    result = cv2.matchTemplate(screenshot_image_gray, template_image_gray, cv2.TM_CCOEFF_NORMED)

    # 일치하는 위치 찾기
    threshold = 0.85
    location = np.where(result >= threshold)

    # 일치하는 이미지가 발견되었는지 확인
    if len(location[0]) > 0:
        # 첫 번째 일치하는 위치 가져오기
        top_left = (location[1][0], location[0][0])
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

        # 이미지에 사각형 그리기
        cv2.rectangle(screenshot_image, top_left, bottom_right, (0, 255, 0), 2)

        # 인식된 이미지를 포함한 캡처 이미지 저장
        # recognized_image_path = 'recognized_image.png'
        # cv2.imwrite(recognized_image_path, screenshot_image)

        # 결과 반환
        # return recognized_image_path
        return top_left

    # 일치하는 이미지가 없을 경우 None 반환
    return '(0,0)'

coord_string = capture_and_recognize_image('02_cj_ssj_dbg_gs_cj_ss_cd.png')  # 주어진 좌표 문자열
# x = coord_string.split(',')[0]
# y = coord_string.split(',')[1]
# print(str(x).replace('(', ''))
print(coord_string)