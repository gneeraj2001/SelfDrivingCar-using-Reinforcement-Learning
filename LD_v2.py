# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 09:29:31 2021

@author: gopal.alc
"""

import numpy as np
from statistics import mean
import math

import cv2

 
# Create a video capture object, in this case we are reading the video from a file

video_capture = cv2.VideoCapture(0)

video_capture.set(cv2.CAP_PROP_FRAME_WIDTH,800) # set the width to 320 p
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT,400) # set the height to 240 p
size = (640,480)
result = cv2.VideoWriter('filename.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)


low_green = np.array([25, 52, 72])
high_green = np.array([102, 255, 255])

def best_fit_slope(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    return m

while(True):
    ret,frame = video_capture.read()
    width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH )
    height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT )
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)

    # Capture the frames

    # Crop the image

#    crop_img = frame[60:120, 0:160]


  

    # Convert to grayscale

    gray = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)


    

    # Color thre
 #   cv2.rectangle(mask, (0, 400), (1000, 750), 255, -1)
    
    #masked = cv2.bitwise_and(frame, frame, mask=mask)
    
 #   vertices = np.array([[0,0], [50,150], [150,150], [150,50]])
 #   vertices = np.int32([vertices])
 
    
 
    #cropped = blur[400:800, 0:1100]
    
    # specify coordinates of the polygon
#    polygon = np.array([[0,500], [250,400], [800,400], [1500,1280]])

    A = np.array([740,300])
    B = np.array([50,300])
    C = np.array([0,400])
    D = np.array([800,400])


    polygon = np.array([A, B, C, D])
    stencil = np.zeros_like(blur)
    cv2.fillConvexPoly(stencil, polygon, 1)
    img = cv2.bitwise_and(blur, blur, mask=stencil)
    
    
    
    # Find the contours of the frame
    ret,thresh = cv2.threshold(img,63,255,cv2.THRESH_BINARY)
    
#    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
    
    contours,hierarchy =  cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    


    # Find the biggest contour (if detected)
    # contours[:][:][0][0][0]= contours[:][:][0][0][0]*2.25
    # contours[:][:][0][0][1]= contours[:][:][0][0][1]*2.25
    
    # for i in range(len(contours)):
    #     contours[i][:,0,1]=contours[i][:,0,1]+ 400


    #print(contours)

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)

        M = cv2.moments(c)

 

        # cx = int(M['m10']/M['m00'])

        # cy = int(M['m01']/M['m00'])


#        cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)

#        cv2.line(frame,(0,cy),(1280,cy),(255,0,0),1)

        cv2.drawContours(frame, contours, -1, (0,255,0), cv2.FILLED)

 

    #     if cx >= 120:

    #         print("Turn Left!")

    #     if cx < 120 and cx > 50:
    #         print("On Track!")

    #     if cx <= 50:
    #         print("Turn Right")
    # else:
    #     print("I don't see the line")

 

    #Display the resulting frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    for cnt in contours :
  
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
      
        # draws boundary of contours.
        #cv2.drawContours(frame, [approx], 0, (0, 0, 255), 5) 
      
        # Used to flatted the array containing
        # the co-ordinates of the vertices.
        n = approx.ravel() 
        #print("####$$$$$$$$$$$$$$$$$$$$$$$")
        #print(n)
        i = 0
        x=[]
        y=[]
        for j in n :
            if(i % 2 == 0):
                # x = n[i]
                # y = n[i + 1]
                x.append(n[i])
                y.append(n[i + 1])
                #print(n.size, "x =", x, "y =", y)
            i = i + 1
        
        x=np.array(x)
        y=np.array(y)
        if(x.size > 2) and (y.size > 2):
            #cv2.putText(frame, "Angle", (x[0], y[0]),font, 0.5, (0, 255, 255)) 
            #slope = best_fit_slope(x,y)
            z= np.polyfit(x,y,1)
            #print(x, y)
            slope = z[0]
            angle = np.rad2deg(math.atan(slope))
            if(math.isnan(slope)):
                
                print("nan")
            else:
                angle = round(angle) +90
                cv2.putText(frame, str(angle), (x[0], y[0]),
                                font, 0.5, (0, 255, 255))

                
            #print("slope = ", slope, "angle = ", angle)

    cv2.imshow('frame',frame)
    print(ret)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break