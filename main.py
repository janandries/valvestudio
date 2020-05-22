import numpy as np
import cv2
import pytesseract

# Load an color image in grayscale
image = cv2.imread('resource/simple.jpg',0)


width = 640
height = 480

orig = image.copy()

x = 170
y = 204
w = 196
h = 158
cropped = image[y:y+h, x:x+w]

cv2.imshow('image',cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

text = pytesseract.image_to_string(cropped) 

print(text)