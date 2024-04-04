import cv2

# Input video file
input_video_path = r'C:\Users\aram_\OneDrive\Рабочий стол\Corners_and_edges\Tracking_Corners_mod.mp4'

cap = cv2.VideoCapture(input_video_path)

while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('Frame', frame)
    cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
