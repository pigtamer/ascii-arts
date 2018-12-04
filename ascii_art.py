import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
# import matplotlib.pyplot as plt

# Define autocanny function, a opensource solution. Computes the median grayscale of the global image then adjust the canny thresholds accordingly.
def autoCanny(image, sigma = 0.33):
	# compute the median of the single channel pixel intensities
    v = np.median(image)
	# apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv.Canny(image, lower, upper)
	# return the edged image
    return edged

# Define the votter for Hog algorithm. 
def votter(vec):
    OrientAdder = np.zeros((5))
    for k in range(len(vec.flatten())):
        item = vec.flatten()[k]
        if item == 0:
            pass
        else:
            if (item > -22.5 and item < 22.5):
                OrientAdder[0] += 1
            elif (item > 67.5 and item <= 90) or (item < -67.5 and item >= -90):
                OrientAdder[1] += 1
            elif (item > 22.5 and item < 67.5):
                OrientAdder[2] += 1
            elif (item > -67.5 and item < -22.5):
                OrientAdder[3] += 1
            else:
                pass
        # print(OrientAdder, "xx")
    return np.argmax(OrientAdder)


# Funtion for the implementation of hogger characterizer.
def hogger(img, cellsize = 3, MODE = 1):
    thefile = open('ascii_art.txt', 'w')
    eps = 1E-4
    rows, cols = img.shape
    rows, cols = int(rows / cellsize), int(cols /cellsize)
    gradRecord = []

    for k in range(0, rows):
        lirow = []
        for j in range(0, cols):
            patch = img[k*cellsize : (k+1)*cellsize, j*cellsize : (j+1)*cellsize]
            Gx = cv.Sobel(patch, cv.CV_64F, 1, 0, ksize=3)
            Gy = cv.Sobel(patch, cv.CV_64F, 0, 1, ksize=3)

            theta = np.arctan(Gx / (Gy + eps))*180/np.pi

            idd = votter(theta)
            if idd == 0:
                morechar = "=" * MODE
            elif idd == 1:
                morechar = "|" * MODE
            elif idd == 2:
                morechar = "/" * MODE
            elif idd == 3:
                morechar = "\\" * MODE
            else:
                pass

            # morechar = chr(np.random.randint(42, 122))*MODE

            if np.sum(patch) == 0:
                morechar = " " * MODE

            if j == 0:
                morechar = "." * MODE
            lirow.append(morechar)
            thefile.write("%s" % morechar)

        thefile.write('\n')
        gradRecord.append(lirow)

    return gradRecord


# Main

SCALE_FLAG, SCALE_FACTOR = True, 1 # whether to scale the input image
CANNY_LOWER, CANNY_UPPER = 10, 100 # manually set canny upper and lower thresholds
AUTO_CANNY_FLAG = False # to use automatic canny thresholds
DISP_FLAG = True # whether to preview
RESOLUTION = 100 # resolution (lines or cols of the output text)
PREVIEW_WINHEIGHT = 800 # preview window height

root = tk.Tk()
root.withdraw() # do not show the base window of tkinter

while(1):
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)

    img = cv.imread(filename)
    # img = cv.imread("X:/cvImg/blowjob.jpg")
    if len(img.shape) >= 3:
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    WINSIZE = int(np.max(img.shape) / RESOLUTION)
    if WINSIZE <= 1:
        WINSIZE = 3

    if SCALE_FLAG:
        img = cv.resize(img, (int(img.shape[1]* SCALE_FACTOR), int(img.shape[0]*SCALE_FACTOR)))

    # Canny the image
    if AUTO_CANNY_FLAG:
        imgCanny = autoCanny(img, 0.9)
    else:
        imgCanny = cv.Canny(img, CANNY_LOWER, CANNY_UPPER)

    imgCanny[imgCanny != 0] = 255

    grOrientAdder = hogger(imgCanny, WINSIZE, 2)

    cv.imwrite("edge.jpg", 255 - imgCanny)

    if DISP_FLAG:
        cv.imshow("canny", cv.resize(255 - imgCanny, (int(PREVIEW_WINHEIGHT* img.shape[1] / img.shape[0]), PREVIEW_WINHEIGHT)))
        wk = cv.waitKey(0)
        cv.destroyAllWindows()

    if wk == ord('q'):
        exit()