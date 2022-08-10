import cv2
import numpy as np
import time
import pyautogui
import autopy
import HandTrackingModule as htm
import ScreenShot

wCam, hCam = 640, 480
frameR = 50
smoothening = 9

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
flag=0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1, detectionCon=0.5)
wScr, hScr = autopy.screen.size()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    cv2.circle(img, (640,240), radius=5, color=(0, 0, 255), thickness=-1)
    cv2.circle(img, (0,240), radius=5, color=(0, 0, 255), thickness=-1)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)
        if fingers.count(1) == 5:   
            lengthLeft, img, lineInfoLeft = detector.findDistanceTabSwitch(9, img, 'Left')
            lengthRight, img, lineInfoRight = detector.findDistanceTabSwitch(9, img, 'Right')
            if lengthLeft <150 or lengthRight<150:
                pyautogui.keyDown('alt')
                time.sleep(.2)
                pyautogui.press('tab')
                time.sleep(.5)
        elif fingers.count(1) == 0:
            pyautogui.keyUp('alt')       

        if fingers[1] == 1 and fingers[2] == 0 and fingers.count(1) == 1:
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        
        elif fingers[1] == 1 and fingers[2] == 1 and  fingers.count(1) == 2:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
                time.sleep(.2)
            
        # elif fingers[1] == 1 and fingers[0] == 1 and fingers.count(1) ==2:
        #     length, img, lineInfo = detector.findDistance(8, 4, img)
        #     if  length <40:
        #         ScreenShot.takeScreenShot('./ScreenShots/')
                
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()