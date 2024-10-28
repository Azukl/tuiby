import cv2
import numpy as np


count_x = 0

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

while(True):
    ret, frame = cap.read()
    if not ret:
        break
    
    red_mask, red_masked_img = detect_red_color(frame)
    c_frame = getContours(red_masked_img, 50)
    if None == c_frame:
        print("bakayarou!!")
    else:
        if c_frame <= 92:
            print(1)
        elif c_frame <= 184:
            print(2)
        elif c_frame <= 276:
            print(3)
        elif c_frame <= 368:
            print(4)
        elif c_frame <= 460:
            print(5)
        elif c_frame <= 552:
            print(6)
        elif c_frame <= 650:  # ataiwokaeru
            print(7)
        
    
    cv2.imshow('Frame', frame)
    cv2.imshow('red', red_masked_img)
    cv2.imshow('test', red_mask)
    
    key = cv2.waitKey(1)
    
    if key == ord('q'):
        break
    if key == ord('s'):
        path = "photo"+ str(count) + ".jpg"
        count += 1
        cv2.imwrite(path,frame)

cap.release()
cv2.destroyAllWindows()
