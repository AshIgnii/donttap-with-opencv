import sys
sys.path.append('d:\!programming\python\python 3.10.0\lib\site-packages')

import time
import cv2
import numpy as np
import pyautogui
from mss import mss

height = 1080
width = 1920

heightDiv = int(height/4 - 30)
widthDiv = int((width/5)*2 - 135)

mon = {'top': heightDiv, 'left': widthDiv, 'width': 650, 'height': 640}

def click(x, y):  # function to click
    print('click')
    pyautogui.failSafeCheck()
    pyautogui.click(x + widthDiv, y + heightDiv, 1, 0, 'left')

startTime = time.time()

with mss() as sct:
    # mon = sct.monitors[0]
    while True:
        last_time = time.time()  # image processing

        img = sct.grab(mon)
        hsv = cv2.cvtColor(np.float32(img), cv2.COLOR_BGR2HSV)
        blk = np.array([0, 0, 0])
        threshold_level = 254
        mask = cv2.inRange(hsv, blk, blk)

        dx = cv2.Scharr(mask, cv2.CV_16SC1, 1, 0)
        dy = cv2.Scharr(mask, cv2.CV_16SC1, 0, 1)
        cu = cv2.Canny(dx, dy, 0, 256)

        thresh = cv2.threshold(cu, 0, 0, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(cu, 1, 2)

        if not len(contours) > 0:
            cu2 = cu
        else:
            cnt = contours[0]  # finding first square center
            np.squeeze(cnt)
            M = cv2.moments(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            cu2 = cv2.rectangle(hsv, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if M['m10'] == 0 or M['m00'] == 0:
                cx = 0
            else:
                cx = int(M['m10'] / M['m00'])
            if M['m01'] == 0 or M['m00'] == 0:
                cy = 0
            else:
                cy = int(M['m01'] / M['m00'])

            if cx > 0 or cy > 0:
                cc1 = cv2.circle(hsv, (cx, cy), 20, (0, 255, 0,), 1)

            if len(contours) > 1:  # finding second square center
                cnt2 = contours[1]
                np.squeeze(cnt2)
                M2 = cv2.moments(cnt2)
                # print(M)
                x2, y2, w2, h2 = cv2.boundingRect(cnt2)
                cu3 = cv2.rectangle(hsv, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)

                if M2['m10'] == 0 or M2['m00'] == 0:
                    cx2 = 0
                else:
                    cx2 = int(M2['m10'] / M2['m00'])
                if M2['m01'] == 0 or M2['m00'] == 0:
                    cy2 = 0
                else:
                    cy2 = int(M2['m01'] / M2['m00'])

                if cx2 > 0 or cy2 > 0:
                    cc2 = cv2.circle(hsv, (cx2, cy2), 20, (0, 255, 0,), 1)

        print('fps: {0}'.format(1 / (time.time() - last_time)))  # shows fps

        try:  # clicking in the squares
            if 'cx' in globals():
                if cx > 0 or cy > 0:
                    click(cx, cy)
                elif cx2 > -1 or cy2 > -1:
                    click(cx2, cy2)
                else:
                    print('No Target Found!')
            else:
                print('No Centers')

        except KeyboardInterrupt:
            break

        #cv2.imshow('HSV', np.array(cu2)) #makes the code slow, only use it for debugging
        #cv2.imshow('Canny', np.array(cu))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            # cv2.destroyAllWindows()
            break
        if time.time() - startTime >= 32: #the script stops after 32 seconds have passed
            break