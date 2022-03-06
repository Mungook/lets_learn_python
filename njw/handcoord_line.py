import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
tracking = np.zeros([10,2])
iteration = 0

# For webcam input:
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)
    image_height, image_width, _ = image.shape
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        # Here is How to Get All the Coordinates
        for ids, landmrk in enumerate(hand_landmarks.landmark):
            #print(ids, landmrk)
            if ids == 8 :
              cx, cy = landmrk.x * image_width, landmrk.y*image_height
              #print(cx, cy)
              #print (ids, cx, cy)
              if iteration < 9:
                tracking[0,0] = cx
                tracking[0,1] = cy
                tracking[iteration+1,0] = tracking[iteration,0]
                tracking[iteration+1,1] = tracking[iteration,1]
              elif iteration >=9:
                    tracking[0,0] = cx
                    tracking[0,1] = cy
                    tracking[4,0] = tracking[3,0]
                    tracking[4,1] = tracking[3,1]
                    tracking[3,0] = tracking[2,0]
                    tracking[3,1] = tracking[2,1]
                    tracking[2,0] = tracking[1,0]
                    tracking[2,1] = tracking[1,1]
                    tracking[1,0] = tracking[0,0]
                    tracking[1,1] = tracking[0,1]
              #tracking 부분에 점을 찍는다.
              #mp_drawing.draw_landmarks(image, hand_landmarks)    #mp_hands.HAND_CONNECTIONS : 점을 이어주는 선
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()