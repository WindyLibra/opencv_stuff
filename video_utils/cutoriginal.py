import cv2
 # ВНИМАНИЕ!!! сделай и поменяй папку
filename_fold = 'DJI_0036_track'
filename_vid = filename_fold + '.mp4'

capture = cv2.VideoCapture(fr"C:\Users\aram_\OneDrive\Documents\{filename_vid}")

frameNr = 1

while (True):

    success, frame = capture.read()

    if success:
        cv2.imwrite(fr'C:\Users\aram_\OneDrive\Documents\{filename_fold}\{filename_fold}_{frameNr}.jpg', frame)
        print(f'Frame No. {frameNr}')

    else:
        break

    frameNr = frameNr + 1

capture.release()

# Получилось)))))!!! Это я сам написал =P
# Вот только папку самому создавать надо