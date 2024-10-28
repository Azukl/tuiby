import cv2
import numpy as np

# 赤色の検出
def detect_red_color(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 赤色のHSVの値域1
    hsv_min = np.array([174,77,235])
    hsv_max = np.array([179,161,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色領域のマスク（255：赤色、0：赤色以外）    
    mask = mask1 

    # マスキング処理
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img

# 入力画像の読み込み
img = cv2.imread(r"C:\Users\g020c1172\Downloads\test_photo.jpg")
# 色検出（赤、緑、青）
red_mask, red_masked_img = detect_red_color(img)

# 結果を出力
cv2.imwrite(r"C:\Users\g020c1172\.vscode\ble\maskred_mask.png", red_mask)
cv2.imwrite(r"C:\Users\g020c1172\.vscode\ble\maskred_masked_img.png", red_masked_img)