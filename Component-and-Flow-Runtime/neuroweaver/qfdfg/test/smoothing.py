import numpy as np
import cv2
import os

def save_image(image, filename):
    cv2.imwrite(filename, image)

with Component() as main:
    img_dir = '/Users/joon/ohai.src/datasets/img'
    image_files = [os.path.join(img_dir, image_file) for image_file in os.listdir(img_dir)]
    img = cv2.imread(image_files[0])
    with Component(inputs=[image_files], outputs=[grayscaled]) as grayscale:
        grayscaled = cv2.cvtColor(image_files, cv2.COLOR_BGR2GRAY)
        save_image(grayscaled, 'grayscaled.jpg')
    gray_img = grayscale(img)
    with Component(inputs=[img], outputs=[blurred]) as blur:
        blurred = cv2.blur(img, (3,3))
        gaussian = cv2.GaussianBlur(blurred, (3,3), 0)
        median = cv2.medianBlur(gaussian, 5)
        bilateral = cv2.bilateralFilter(median, 5, 25, 25)
        save_image(bilateral, 'blurred.jpg')
        blurred = bilateral
    blurred = blur(gray_img)

main()
