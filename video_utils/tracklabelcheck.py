import cv2

# Read the video file
video_file = r'C:/Users/aram_/OneDrive/Рабочий стол/Tracking_Corners.mp4'
cap = cv2.VideoCapture(video_file)
if not cap.isOpened():
    print("something's wrong i can feel it")

# Read coordinates from the text file and draw rectangles on the video
with open(r'C:/Users/aram_/PycharmProjects/PrepareDataForTracking/txt_files/Tracking_Corners.txt', 'r') as file:
    for line in file:
        # Split the line into coordinates
        coords = line.split()

        # Ensure the line has 4 coordinates
        if len(coords) == 4:
            xmin, ymin, xmax, ymax = map(int, coords)
            try:
                ret, frame = cap.read()
                if ret:
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                    cv2.imshow('Video with Rectangles', frame)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
            except ValueError:
                continue

        if len(coords) == 5:
            war, xmin, ymin, xmax, ymax = map(int, coords)
            try:
                ret, frame = cap.read()
                if ret:
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                    cv2.imshow('Video with Rectangles', frame)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
            except ValueError:
                continue



# Release VideoCapture object
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()





