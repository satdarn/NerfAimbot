import numpy as np
import cv2
import serial
import time

Serial = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=10)
cap = cv2.VideoCapture(2)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
trigger_thresshold = 50

def send(data):
    Serial.write(bytes(data, 'utf-8'))
    time.sleep(0.05)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))
    centerX = int(width/2)
    centerY = int(height/2)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    crosshairX = cv2.line(frame, (0, centerY), (width, centerY), (0,0,144), 10)
    crosshairY = cv2.line(frame, (centerX, 0), (centerX, height), (0,0,144), 10)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        face_center = [int(x+(w/2)),int(y+(h/2))]
        cv2.circle(frame, (face_center[0],face_center[1]), 10, (255,255,255),-1 )
        send("1")
        roi_gray = gray[y:y+w, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
        if centerX-trigger_thresshold < face_center[0] < centerX+trigger_thresshold:
            img = cv2.putText(frame, '  Y', (10, height - 10), font, 2, (255, 255, 255), 5, cv2.LINE_AA)
        if centerY-trigger_thresshold < face_center[1] < centerY+trigger_thresshold:
            img = cv2.putText(frame, 'X  ', (10, height - 10), font, 2, (255, 255, 255), 5, cv2.LINE_AA)
        if centerX-trigger_thresshold < face_center[0] < centerX+trigger_thresshold and centerY-trigger_thresshold < face_center[1] < centerY+trigger_thresshold:
            img = cv2.putText(frame, '     FIRE', (10, height - 10), font, 3, (0, 0, 255), 5, cv2.LINE_AA)
            send("2")
    cv2.imshow('frame', frame)
    send("0")
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
