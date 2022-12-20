# 샘플 Python 스크립트입니다.

# Shift+F10을(를) 눌러 실행하거나 내 코드로 바꿉니다.
# 클래스, 파일, 도구 창, 액션 및 설정을 어디서나 검색하려면 Shift 두 번을(를) 누릅니다.
import pyautogui
import pyaudio
import numpy as np

CHUNK = 2 ** 10
RATE = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 1
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()


def check_and_land():
    p = pyaudio.PyAudio()

    # for index in range(p.get_device_count()):
    #     desc = p.get_device_info_by_index(index)
    #     print(desc)
    #     print("DEVICE: {device}, INDEX: {index}, RATE: {rate} ".format(
    #         device=desc["name"], index=index, rate=int(desc["defaultSampleRate"])))

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK, input_device_index=1)
    frames = []
    while (True):
        datasrc = stream.read(CHUNK)
        # data = np.fromstring(datasrc, dtype=np.int16)
        data = np.frombuffer(datasrc, dtype=np.int16)
        frames.append(datasrc)
        if np.average(np.abs(data)) > 500:
            print(int(np.average(np.abs(data))))
            return True

def action():

    img_capture = pyautogui.locateOnScreen(r"img\target1.png", confidence=0.7)  #, region=(1800, 0, 1920, 100))
    print(img_capture)
    #pyautogui.press('f5')
    pyautogui.moveTo(img_capture)
    if(check_and_land()) :
        pyautogui.rightClick()


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    action()

# https://www.jetbrains.com/help/pycharm/에서 PyCharm 도움말 참조
