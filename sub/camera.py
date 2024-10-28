import cv2

cap = cv2.VideoCapture(-1)
count = 0

while(True):
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imshow('Frame',frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    if key == ord('s'):
        count += 1
        path = "photo"+ str(count) + ".jpg"
        cv2.imwrite(path,frame)

cap.release()
cv2.destroyAllWindows()
