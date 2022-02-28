import numpy as np
import cv2

col_obj = ()

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
    
def click_data(event, x, y, flags, param):

  if (event == cv2.EVENT_LBUTTONDOWN):
     blue = frame[y,x,0];
     green = frame[y,x,1];
     red = frame[y,x,2];
     print(rgb_to_hsv(red, green, blue))
    # print(frame)


cap = cv2.VideoCapture(0)

cv2.namedWindow("images")
cv2.setMouseCallback("images",click_data) 
#  HSV pixel의 lower과 upper 경계값 정의/스킨 색 경계값 설정
# 'skin'의 범위 값 설정 
#lower = np.array([0, 48, 80], dtype = "uint8")
#upper = np.array([20, 255, 255], dtype = "uint8")

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
        
    _, frame = camera.read()
    under_col = []
    upper_col = []

    for i in range(3):
        under_col.append(col_obj[i]-5)
        upper_col.append(col_obj[i]+5)
        if(under_col[i] < 0):
            under_col[i] = 0
        if(upper_col[i] > 179):
            if(i>0):
                if(upper_col[i] > 255):
                    upper_col[i] = 255
                else:
                    upper_col[i] = 179

    lower = np.array([under_col[0], under_col[1], under_col[2]])
    upper = np.array([upper_col[0], upper_col[1], upper_col[2]])

    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
 
    # 경계선 찾아주는애
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))#타원 모양으로 매트리스 생성
    skinMask = cv2.dilate(skinMask, kernel, iterations = 1)#SkinMask의 iterations를 두번 반복(잡힌 범위 주변 margin이 뚱뚱해진다)
 
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    
    
    #print(cv2.findContours(skinMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE))

    line, _= cv2.findContours(skinMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #print(line)
    cv2.drawContours(frame, line, -1, (0,255,0), 3)#(라인을 그릴 이미지, 검출된 컨투어, 음수로 지정할경우 모든 컨투어,색상지정(현재는 초록),선두께)

    cv2.imshow("images",frame)
 
    # q누르면 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()