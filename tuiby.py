import cv2
import bluepy
import numpy as np
import sys, tty, termios, os, time
import threading
import BTS7960BHBridge as HBridge
import RPi.GPIO as GPIO
from time import sleep

count_x = 0
count_y = 0
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
    count_y = 0
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   
    #一つ以上検出
    if len(contours) > 0:
        for cnt in contours:
            c = cnt[0][0]
            print(c)
            if count_x < c[0]:
                count_x = c[0]
            if count_y < c[1]:
                count_y = c[1]
        return int(count_x), int(count_y)
            
            
def control(test):
    global cancel
    global RSSI
    global count
    global lig
    add = 0
    cres = 0
    t3.start()
    while(True):
        print(RSSI)
        if RSSI == 100:
            print("hello")
            speedleft = 0
            speedright = 0
            HBridge.setMotorLeft(speedleft)
            HBridge.setMotorRight(speedright)
            #
            lig = 1
        # else:
        #print(test)
        ret, frame = cap.read()
        #if not ret:
            #   break
        
        red_mask, red_masked_img = detect_red_color(frame)
        c_frame = getContours(red_masked_img, 50)

        if None == c_frame and cancel == 40:
            print("stop")
            speedleft = 0
            speedright = 0
            HBridge.setMotorLeft(speedleft)
            HBridge.setMotorRight(speedright)
            lig = 1
            time.sleep(0.3)
        elif None == c_frame:
            print("bakayarou!!")
            cancel += 1
        else:
            lig = 0
            cancel = 0
            if c_frame[1] <= 150:
                add = -0.2 
            elif c_frame[1] <= 300:
                add = 0.1  * cres
            elif c_frame[1] <= 450:
                add = 0.3  * cres

            if c_frame[0] <= 92:
                speedleft = 0.6 + add
                speedright = 0.4 + add
                HBridge.setMotorLeft(speedleft)
                HBridge.setMotorRight(speedright)
                print("a")
            elif c_frame[0] <= 174: # -10
                speedleft = 0.6 + add
                speedright = 0.5 + add
                HBridge.setMotorLeft(speedleft)
                HBridge.setMotorRight(speedright)
                print("b")
            elif c_frame[0] <= 266: # -10
                speedleft = 0.6 + add
                speedright = 0.55 + add
                HBridge.setMotorLeft(speedleft)
                HBridge.setMotorRight(speedright)
                print("c")
            elif c_frame[0] <= 408: # +40
                speedleft = 0.6 + add
                speedright = 0.6 + add
                HBridge.setMotorLeft(speedleft)
                HBridge.setMotorRight(speedright)
                print("center")
            elif c_frame[0] <= 470: # +10
                speedleft = 0.55 + add
                speedright = 0.6 + add
                HBridge.setMotorLeft(speedleft)
                HBridge.setMotorRight(speedright)
                print("d")
            elif c_frame[0] <= 562: # +10
                speedleft = 0.5 + add
                speedright = 0.6 + add
                HBridge.setMotorLeft(speedleft)
                HBridge.setMotorRight(speedright)
                print("e")
            elif c_frame[0] <= 650:  # ataiwokaeru
                speedleft = 0.4 + add
                speedright = 0.6 + add
                HBridge.setMotorLeft(speedleft)
                HBridge.setMotorRight(speedright)
                print("f")
            
           # cv2.imshow('Frame', frame)
           # cv2.imshow('red', red_masked_img)
           # cv2.imshow('test', red_mask)
            
            key = cv2.waitKey(1)
            count += 1
            if count <= 100:
                cres = count / 100
            
            #if key == ord('q') or cancel == 30:
                # speedleft = 0
                # speedright = 0
                # HBridge.setMotorLeft(speedleft)
                # HBridge.setMotorRight(speedright)

def scan(py):
    global RSSI
    global cancel
    #print(py)
    while(True):
        GPIO.output(led_port, GPIO.HIGH)
        print("high")
        scanner = bluepy.btle.Scanner(0)
        devices = scanner.scan(3)
        for device in devices:
            if device.addr == "f9:49:3e:93:cf:25":
                print('======================================================')
    #           print('address : %s' % device.addr)
    #           print('addrType: %s' % device.addrType)
                print('RSSI    : %s' % device.rssi)
                RSSI = device.rssi
                if RSSI >= -45:
                    print("world")
                    RSSI = 100
                # elif RSSI >= -45 and count_y <= 30:
                #     print("upper")
                #     RSSI = 100
                
        #           print('Adv data:')
                 # for (adtype, desc, value) in device.getScanData():
                 #   print(' (%3s) %s : %s ' % (adtype, desc, value))
        # key = cv2.waitKey(1)
        
        # if key == ord('q') or cancel == 30:
        #     #break

# class Light():
#     global lig
#     def __init__(self):
#         self.stoped = threading.Event()

#     def stop(self):
#         self.stoped.set()

#     def start():
#         while(True):
#             GPIO.output(led_port, GPIO.HIGH)
#             if lig == 1:
#                 GPIO.output(led_port, GPIO.HIGH)
#                 print("high")
#                 sleep(0.5)
#                 GPIO.output(led_port, GPIO.LOW)
#                 print("low")
#                 sleep(0.5)

#     def blink():
#         GPIO.output(led_port, GPIO.HIGH)
#         print("high")
#         sleep(0.5)
#         GPIO.output(led_port, GPIO.LOW)
#         print("low")
#         sleep(0.5)

def light():
    while(True):
        global lig
        GPIO.output(led_port, GPIO.HIGH)
        #print("lig:",lig)
        if lig == 1:
            GPIO.output(led_port, GPIO.HIGH)
            print("high")
            sleep(0.5)
            GPIO.output(led_port, GPIO.LOW)
            print("low")
            sleep(0.5)



cap = cv2.VideoCapture(0)
count = 0
cancel = 0
RSSI = 0
lig = 0
t1 = threading.Thread(target=control, args=("t1",))
t2 = threading.Thread(target=scan, args=("t2",))
#t3 = threading.Thread(target=Light)
t3 = threading.Thread(target=light)

led_port = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_port, GPIO.OUT)

while(True):
    print("device scan...")
    scanner = bluepy.btle.Scanner(0)
    devices = scanner.scan(3)
    for device in devices:
            if device.addr == "f9:49:3e:93:cf:25":

                GPIO.output(led_port, GPIO.HIGH)
                t2.start()
                t1.start()
                t1.join()
                t2.join()
                
    key = cv2.waitKey(1)
        
    if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
