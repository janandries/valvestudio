import numpy as np
import imutils
import cv2
import pytesseract

from digits import DIGITS_LOOKUP
from transforms import four_point_transform

# Load an color image in grayscale
image = cv2.imread('resource/img01.jpg',0)
width = 640
height = 480
orig = image.copy()

# pre-process the image by resizing it, converting it to
# graycale, blurring it, and computing an edge map
#image = imutils.resize(image)
blurred = cv2.GaussianBlur(image, (5, 5), 0)
edged = cv2.Canny(blurred, 0, 106)

cv2.imshow('edged',edged)

# find contours in the edge map, then sort them by their
# size in descending order
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# if the contour has four vertices, then we have found
	# the thermostat display
	if len(approx) == 4:
		displayCnt = approx
		break





## Crop the image to only include our LCD
#x = 170
#y = 204
#w = 196
#h = 158
#cropped = image[y:y+h, x:x+w]

#cv2.imshow('image',cropped)

#cv2.approxPolyDP
# extract the thermostat display, apply a perspective transform
# to it
#warped = four_point_transform(gray, displayCnt.reshape(4, 2))
output = four_point_transform(image, displayCnt.reshape(4, 2))



cv2.imshow('warped', output)

# threshold the warped image, then apply a series of morphological
# operations to cleanup the thresholded image
thresh = cv2.threshold(warped, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

cv2.imshow('thresh', thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()




#recognize text
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string(cropped) 
print(text)