import pyautogui
from PIL import ImageGrab

while 1:
    screen = ImageGrab.grab() # 화면 캡쳐
    print(screen.getpixel(pyautogui.position()))#현재의 마우스 위치의 색상 출력.