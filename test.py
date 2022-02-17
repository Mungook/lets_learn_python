import cv2
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End")
        break
        
    cv2.imshow('video' , frame)
    if cv2.waitKey(1) == ord('q'):
        print('사용자 입력에 의해 종료')
        break
cap.release()
cv2.destroyAllWindows()