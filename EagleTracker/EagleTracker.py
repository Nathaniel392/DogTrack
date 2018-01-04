import libjevois as jevois
import cv2
import numpy as np
import json

#Holders for target data
pixels = [(0,0), (0,0), (0,0), (0,0)]

##Threshold values for Trackbars, These are pulled from the CalFile
CalFile = open ('Calibration').read().split(",")

errode = int(CalFile[0])
dilate = int(CalFile[1])
approx = int(CalFile[2])
area = int(CalFile[3])
solidity = float(CalFile[4])
ratio = float(CalFile[5])


class EagleTracker:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("Catbox", 100, jevois.LOG_INFO)
        
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR by default. If
        # you need a grayscale image instead, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB()
        # and getCvRGBA():
        inimg = inframe.getCvBGR()
        
        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()

        ## Split into red, green, and blue, subtract red from the green
        b,g,r=cv2.split(inimg)
        binImage=g-r
        #Otsu's is a dynamic threshold that does a good job of isolating. Not as fast as fixed
        ret3,binImage = cv2.threshold(binImage,0,255,cv2.THRESH_OTSU)
        
        # Erode image to remove noise if necessary.
        binImage = cv2.erode(binImage, None, iterations = errode)
        #Dilate image to fill in gaps
        binImage = cv2.dilate(binImage, None, iterations = dilate)
        
        ##Finds contours (like finding edges/sides), 'contours' is what we are after
        im2, contours, hierarchy = cv2.findContours(binImage, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
        
        ##arrays to will hold the good/bad polygons
        squares = []
        badPolys = []
        
        ## Parse through contours to find targets
        for c in contours:
            if (contours != None) and (len(contours) > 0):
                cnt_area = cv2.contourArea(c)
                hull = cv2.convexHull(c , 1)
                hull_area = cv2.contourArea(hull)  #Used in Solidity calculation
                p = cv2.approxPolyDP(hull, approx, 1)
                x,y,w,h = cv2.boundingRect(c)
                aspect_ratio = float(w)/h
                if (cv2.isContourConvex(p) != False) and (len(p) == 4) and (cv2.contourArea(p) >= area): #p=3 triangle,4 rect,>=5 circle
                    filled = cnt_area/hull_area
                    if filled <= solidity: #Used to determine if target is hollow or not
                        if aspect_ratio >= ratio:
                            squares.append(p)
                        
                else:
                    badPolys.append(p)
       
        
        ##BoundingRectangles are just CvRectangles, so they store data as (x, y, width, height)
        ##Calculate and draw the center of the target based on the BoundingRect

        if len(squares) > 0:
            i=1
            cv2.putText(inimg, "Tracking", (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),1, cv2.LINE_AA)
            pixels = {"Trk" : len(squares)} #Start of pixels array, values added in the loop for each contour
            for s in squares:
                br = cv2.boundingRect(s)
                #Target "x" and "y" center 
                x = br[0] + (br[2]/2)
                y = br[1] + (br[3]/2)
                #Build "pixels" array to contain info desired to be sent to RoboRio
                pixels['XCntr_'+str(i)]=x
                pixels['YCntr_'+str(i)]=y    
                cv2.rectangle(inimg, (br[0],br[1]),((br[0]+br[2]),(br[1]+br[3])),(0,0,255), 2,cv2.LINE_AA)
                i=i+1   
                
                
        if not squares:
            pixels = {"Trk" : 0, "XCntr_1" : 0, "YCntr_1" : 0}
            cv2.putText(inimg, "Not Tracking", (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),1, cv2.LINE_AA)
            
            
        outimg = inimg
        
     
        
        # Write frames/s info from our timer into the edge map (NOTE: does not account for output conversion time):
        fps = self.timer.stop()
        height, width, channels = outimg.shape # if outimg is grayscale, change to: height, width = outimg.shape
        cv2.putText(outimg, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

        # Convert our BGR output image to video output format and send to host over USB. If your output image is not
        # BGR, you can use sendCvGRAY(), sendCvRGB(), or sendCvRGBA() as appropriate:
        
        outframe.sendCvBGR(outimg,50)
        json_pixels = json.dumps(pixels) 
        jevois.sendSerial(json_pixels)
