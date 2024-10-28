import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

while(1):
    re, frame = cap.read()
    original = frame.copy()

    def getMask(l, u):
        # HSV変換
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # 指定した色の下限
        lower = np.array(l)#([0, 208, 94], dtype=”uint8″)
        # 指定した色の上限
        upper = np.array(u)#([179, 255, 232], dtype=”uint8″)
        # 指定した色の画素を 255、それ以外の画素を0として2値化を行う関数
        mask = cv2.inRange(image, lower, upper)
        return mask

    def getContours(mask):
        # 輪郭抽出
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # バージョンに応じて輪郭抽出する
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        if len(cnts) > 0:
            # 等高線を反復処理し、頂点の数でフィルタリングする
            for c in cnts:
            # 周囲長
                perimeter = cv2.arcLength(c, True)
                # 輪郭の近似
                approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
                if len(approx) > 6:
                    umbrella=cv2.drawContours(original, [c], -1, (36, 255, 12), -1)
                    return umbrella
        else:
            return original
    mask = getMask([-20 ,100, 94], [180, 255, 232])
    cv2.imshow('mask', mask)
    cv2.imshow('original', original)
    umbrella_frame = getContours(mask)

    cv2.imshow('umbrellaCnt', umbrella_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        cv2.imwrite('mask.png', mask)
        cv2.imwrite('original.png', original)
    elif key == ord('q'):
        break

cv2.destroyAllWindows()