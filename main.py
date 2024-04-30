import cv2
import numpy as np
import math
import yol

Kırmızı=(0, 0, 255)
Yeşil= (0, 255, 0)
Mavi=(255, 0, 0)
Sarı= (0, 255, 255)
Mor=(128, 0, 128)
Turuncu= (0, 165, 255)
Pembe= (203, 192, 255)
Turkuaz= (208, 224, 64)
Gri= (128, 128, 128)
Bordo= (0, 0, 128)
font = cv2.FONT_HERSHEY_SIMPLEX
org = (00, 185)
fontScale = 1


cap = cv2.VideoCapture("vid1.mp4")

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Merkez noktası x=615 y=360
    roi = frame[200:660, 200:1100]  # frame[y1:y2,x1:x2]
    ret,thresh1 = cv2.threshold(roi, 254, 254, cv2.THRESH_BINARY)
    black = np.zeros(roi.shape, dtype=np.uint8) + 255
    line=cv2.bitwise_and(thresh1,black)


    hsv = cv2.cvtColor(line, cv2.COLOR_BGR2HSV)
    lower_color = np.array([0, 0, 0], dtype=np.uint8)
    upper_color = np.array([100, 100, 100], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_color, upper_color)

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.medianBlur(mask, 15)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    merkez=(660,360)
    cv2.circle(frame,merkez,15,Gri,-1)


    if len(contours) > 0:

        c = yol.findMaxContour(contours)

        Left = tuple(c[c[:, :, 0].argmin()][0])
        Right = tuple(c[c[:, :, 0].argmax()][0])
        Top = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])


        #center=((Right[0]-Left[0])//2+27,(Left[1]-Top[1])//2+1)
        center=(450,220)
        mesafe=math.sqrt((Right[0] - Left[0]) ** 2 + (Right[1] - Left[1]) ** 2)
        mesafe1 = math.sqrt((Top[0] - Left[0]) ** 2 + (Left[1] - Top[1]) ** 2)
        #cv2.circle(roi, center, 15, yellow, -1)

        try:
            a,d=yol.köşe(contours,roi)
            print(d[1][0][0]-d[0][0][0])


            cv2.putText(roi,str(a),org, font, fontScale,Mavi,2,cv2.LINE_AA)
            cv2.circle(roi, d[0][0], 15, Sarı, -1)
            cv2.circle(roi, d[1][0], 15, Kırmızı, -1)
            cv2.circle(roi, d[2][0], 15, Mavi, -1)
            cv2.circle(roi, d[3][0], 15, Mor, -1)
            cv2.circle(roi, d[4][0], 15, Turkuaz, -1)
            cv2.circle(roi, d[5][0], 15, Turuncu, -1)
            cv2.circle(roi, d[6][0], 15, Pembe, -1)
            cv2.circle(roi, d[8][0], 15, Bordo, -1)


        except:
            pass

    cv2.imshow("frame", frame)
    cv2.imshow("roi", roi)




    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()