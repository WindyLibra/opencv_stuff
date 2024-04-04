import cv2

cap = cv2.VideoCapture(r"C:\Users\aram_\OneDrive\Рабочий стол\Corners_and_edges\Corners_and_edges.mp4")

if cap.isOpened() == False:
    print("Error opening video file")

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Frame', frame)
        keyboard = cv2.waitKey(0)

    else:
        break

cap.release()
cv2.destroyAllWindows()