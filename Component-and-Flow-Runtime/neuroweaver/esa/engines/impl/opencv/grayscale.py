import cv2

def grayscale(img_in):
    img_out = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
    return img_out
