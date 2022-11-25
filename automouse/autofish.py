# 샘플 Python 스크립트입니다.

# Shift+F10을(를) 눌러 실행하거나 내 코드로 바꿉니다.
# 클래스, 파일, 도구 창, 액션 및 설정을 어디서나 검색하려면 Shift 두 번을(를) 누릅니다.
import pyautogui

def action():

    img_capture = pyautogui.locateOnScreen(r"img\target1.png", confidence=0.7)  #, region=(1800, 0, 1920, 100))
    print(img_capture)
    pyautogui.press('f5')
    pyautogui.moveTo(img_capture)
    pyautogui.rightClick()

# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    action()

# https://www.jetbrains.com/help/pycharm/에서 PyCharm 도움말 참조
