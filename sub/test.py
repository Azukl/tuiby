import cv2
import numpy as np
import sys, tty, termios, os
import BTS7960BHBridge as HBridge

count_x = 0
speedleft = 0
speedright = 0

# 赤色の検出
def detect_red_color(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 赤色のHSVの値域1
    hsv_min = np.array([170,160,255])
    hsv_max = np.array([179,170,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色領域のマスク（255：赤色、0：赤色以外）    
    mask = mask1 

    # マスキング処理
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img


def getContours(img,t):
    count_x = 0
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #一つ以上検出
    if len(contours) > 0:
        for cnt in contours:
            c = cnt[0][0]
            #count_y = c[1]
            if count_x < c[0]:
                count_x = c[0]
            #print(cv2.contourArea(contours[cnt]))
        return count_x
            
            
            
            
            # 最小外接円を描く
            #(x,y), radius = cv2.minEnclosingCircle(cnt)
            #center = (int(x),int(y))
            #print(center)


cap = cv2.VideoCapture(0)
count = 0
cancel = 0

while(True):
    ret, frame = cap.read()
    if not ret:
        break
    
    red_mask, red_masked_img = detect_red_color(frame)
    c_frame = getContours(red_masked_img, 50)
    if None == c_frame:
        print("bakayarou!!")
        cancel += 1
    else:
        cancel = 0
        if c_frame <= 92:
            speedleft = 0.3
            speedright = 0.1
            HBridge.setMotorLeft(speedleft)
            HBridge.setMotorRight(speedright)
            print("a")
        elif c_frame <= 174: # -10
            speedleft = 0.3
            speedright = 0.2
            HBridge.setMotorLeft(speedleft)
            HBridge.setMotorRight(speedright)
            print("b")
        elif c_frame <= 266: # -10
            speedleft = 0.3
            speedright = 0.25
            HBridge.setMotorLeft(speedleft)
            HBridge.setMotorRight(speedright)
            print("c")
        elif c_frame <= 408: # +40
            speedleft = 0.3
            speedright = 0.3
            HBridge.setMotorLeft(speedleft)
            HBridge.setMotorRight(speedright)
            print("center")
        elif c_frame <= 470: # +10
            speedleft = 0.25
            speedright = 0.3
            HBridge.setMotorLeft(speedleft)
            HBridge.setMotorRight(speedright)
            print("d")
        elif c_frame <= 562: # +10
            speedleft = 0.2
            speedright = 0.3
            HBridge.setMotorLeft(speedleft)
            HBridge.setMotorRight(speedright)
            print("e")
        elif c_frame <= 650:  # ataiwokaeru
            speedleft = 0.1
            speedright = 0.3
            HBridge.setMotorLeft(speedleft)
            HBridge.setMotorRight(speedright)
            print("f")
    
   # cv2.imshow('Frame', frame)
   # cv2.imshow('red', red_masked_img)
   # cv2.imshow('test', red_mask)
    
    key = cv2.waitKey(1)
    
    if key == ord('q') or cancel == 30:
        break
    
cap.release()
cv2.destroyAllWindows()
