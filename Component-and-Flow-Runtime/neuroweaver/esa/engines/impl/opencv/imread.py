import cv2

def imread(img_file):
    img = cv2.imread(img_file, cv2.IMREAD_COLOR)
    return img
