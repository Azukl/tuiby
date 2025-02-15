import cv2
import numpy as np

# 0 <= h <= 179 (色相)　OpenCVではmax=179なのでR:0(180),G:60,B:120となる
# 0 <= s <= 255 (彩度)　黒や白の値が抽出されるときはこの閾値を大きくする
# 0 <= v <= 255 (明度)　これが大きいと明るく，小さいと暗い
# ここaka
LOW_COLOR = np.array([170,160,255])
HIGH_COLOR = np.array([179,161,255])

# 抽出する青色の塊のしきい値
AREA_RATIO_THRESHOLD = 0.005

def find_specific_color(frame,AREA_RATIO_THRESHOLD,LOW_COLOR,HIGH_COLOR):
    """
    指定した範囲の色の物体の座標を取得する関数
    frame: 画像
    AREA_RATIO_THRESHOLD: area_ratio未満の塊は無視する
    LOW_COLOR: 抽出する色の下限(h,s,v)
    HIGH_COLOR: 抽出する色の上限(h,s,v)
    """
    # 高さ，幅，チャンネル数
    h,w,c = frame.shape

    # hsv色空間に変換
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    # 色を抽出する
    ex_img = cv2.inRange(hsv, LOW_COLOR, HIGH_COLOR)

    # 輪郭抽出
    print(ex_img)
    print(cv2.RETR_EXTERNAL)
    print(cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(ex_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 面積を計算
    areas = np.array(list(map(cv2.contourArea,contours)))

    if len(areas) == 0 or np.max(areas) / (h*w) < AREA_RATIO_THRESHOLD:
        # 見つからなかったらNoneを返す
        print("not found red")
        return None
    else:
        # 面積が最大の塊の重心を計算し返す
        max_idx = np.argmax(areas)
        max_area = areas[max_idx]
        result = cv2.moments(contours[max_idx])
        x = int(result["m10"]/result["m00"])
        y = int(result["m01"]/result["m00"])
        return (x,y)

def test():
    img = cv2.imread("sample.jpg")

    # 位置を抽出
    pos = find_specific_color(
        img,
        AREA_RATIO_THRESHOLD,
        LOW_COLOR,
        HIGH_COLOR
    )

    if pos is not None:
        cv2.circle(img,pos,10,(0,0,255),-1)
    
    cv2.imwrite("result.jpg",img)


# webカメラを扱うオブジェクトを取得
cap = cv2.VideoCapture(0)


while True:
    ret,frame = cap.read()

    if ret is False:
        print("cannot read image")
        continue

    # 位置を抽出
    pos = find_specific_color(
        frame,
        AREA_RATIO_THRESHOLD,
        LOW_COLOR,
        HIGH_COLOR
    )

    if pos is not None:
        # 抽出した座標に丸を描く
        cv2.circle(frame,pos,10,(0,0,255),-1)
    
    # 画面に表示する
    cv2.imshow('frame',frame)

    # キーボード入力待ち
    key = cv2.waitKey(1) & 0xFF

    # qが押された場合は終了する
    if key == ord('q'):
        break

cv2.destroyAllWindows()
