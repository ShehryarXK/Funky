#!/usr/bin/env python
# import the necessary packages
#from pyimagesearch.transform import four_point_transform
#from pyimagesearch import imutils
#from skimage.filters import threshold_adaptive
import numpy as np
import scipy.ndimage as nd
import argparse
import cv2
import matplotlib
import time
import rect
from skimage import data, morphology, filter as imfilter
 
# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required = True,
#	help = "Path to the image to be scanned")
#args = vars(ap.parse_args())
# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread('o.jpg')
#ratio = image.shape[0] / 500.0
orig = image.copy()
#image = cv2.resize(image, (1500, 880))
#image = imutils.resize(image, height = 500)
 
# convert the image to grayscale, blur it, and find edges
# in the image
dst = np.zeros(image.shape, image.dtype)
for i in xrange(image.shape[2]):
    dst[:, :, i] = nd.gaussian_filter(image[:, :, i], 5)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

# scikit-image
dst = imfilter.gaussian_filter(image, 5, multichannel=True)
 
# show the original image and the edge detected image
print "STEP 1: Edge Detection"
print image.shape
#cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.imshow("Gauss", dst)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
 
# loop over the contours
for c in cnts:
# approximate the contour
	peri = cv2.arcLength(c, True)
 	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
 	# if our approximated contour has four points, then we
 	# can assume that we have found our screen
 	if len(approx) == 4:
 		screenCnt = approx
 		break

 
# show the contour (outline) of the piece of paper
# print "STEP 2: Find contours of paper"
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()



# mapping target points to 800x800 quadrilateral
approx = rect.rectify(screenCnt)
pts2 = np.float32([[0,0],[800,0],[800,800],[0,800]])

M = cv2.getPerspectiveTransform(approx,pts2)
dst = cv2.warpPerspective(orig,M,(800,800))

cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)


# using thresholding on warped image to get scanned effect (If Required)
ret,th1 = cv2.threshold(dst,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(dst,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(dst,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
ret2,th4 = cv2.threshold(dst,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow("Thres binary", th1)
cv2.imshow("Thres mean", th2)
cv2.imshow("Thres gauss", th3)
cv2.imshow("Outs", th4)
# apply the four point transform to obtain a top-down
# view of the original image
#warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
 
# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
#warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
#warped = threshold_adaptive(warped, 251, offset = 10)
#warped = warped.astype("uint8") * 255
 
# # show the original and scanned images
print "STEP 3: Apply perspective transform"

#cv2.imshow("Original", imutils.resize(orig, height = 650))
#cv2.imshow("Scanned", imutils.resize(warped, height = 650))
#cv2.waitKey(0)
