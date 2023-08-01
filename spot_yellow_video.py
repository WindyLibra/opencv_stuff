#It spots out yellow color (actually any color) in video, shows it and deletes shapes that are smaller than a cetain amount of pixels (approximately?)
import cv2 as cv
import numpy as np

cap = cv.VideoCapture("C:/Users/aram_/OneDrive/Documents/Videos_and_Images_for_Test/For Tracking/Videos/djiMini.mp4")


while True:

    _, frame = cap.read()

    imgray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(frame, contours, -1, (0, 255, 0), 1)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower_yellow = np.array([5, 60, 60])
    upper_yellow = np.array([20, 255, 255])

    yel_mask = cv.inRange(hsv, lower_yellow, upper_yellow)
    cv.imshow('mask for yellow', yel_mask)
    trueyel = cv.bitwise_and(frame, frame, mask=yel_mask)
    cv.imshow('Yellow?', trueyel)

    for contour in contours:
        if cv.contourArea(contour) < 20050: #why 20050 is optimal idk
            cv.drawContours(yel_mask, [contour], -1, 0, 0)
            cv.fillPoly(yel_mask, pts=[contour], color=(0, 0, 0))

    trueyel = cv.bitwise_and(frame, frame, mask=yel_mask)
    cv.imshow('frame', frame)
    cv.imshow('mask', yel_mask)
    cv.imshow('Yellow', trueyel)

    if cv.waitKey(25) & 0xFF == ord('q'):
        break


cv.destroyAllWindows()
cap.release()
