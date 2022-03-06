import cv2
import pyautogui #파일이름을 패키지명이랑 똑같이 만들어놓으면 당연히 실행이 안됨
from PIL import ImageGrab

def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)    #해결방법 검색하니까 바로 제일 위에 나오던데? https://unie2.tistory.com/328
                                            #그리고 이 라인은 while 안에 넣으면 급격히 느려짐 매 루프마다 웹캠을 변수에 넣는거라
cv2.namedWindow('screen')

while 1:
    _,frame = cap.read()
    
    cv2.imshow('screen',frame)
    screen = ImageGrab.grab() # 화면 캡쳐
    print(screen.getpixel(pyautogui.position()))#현재의 마우스 위치의 색상 출력.q
    #print(rgb_to_hsv(screen.getpixel(pyautogui.position())))
    
    if cv2.waitKey(1) == ord('q'):
        print('사용자 입력에 의해 종료')
        break
    
cap.release()
cv2.destroyAllWindows()