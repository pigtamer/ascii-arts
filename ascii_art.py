import cv2 as cv
import numpy as np
# import matplotlib.pyplot as plt

def votter(vec):
    adder = np.zeros((5))
    for k in range(len(vec.flatten())):
        item = vec.flatten()[k]
        if item == 0:
            pass
        else:
            if (item > -22.5 and item < 22.5):
                adder[0] += 1
            elif (item > 67.5 and item <= 90) or (item < -67.5 and item >= -90):
                adder[1] += 1
            elif (item > 22.5 and item < 67.5):
                adder[2] += 1
            elif (item > -67.5 and item < -22.5):
                adder[3] += 1
            else:
                pass
        # print(adder, "xx")
    return np.argmax(adder)



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

DISP_FLAG = False
SCALE_FLAG, SCALE_FACTOR = False, 2
CANNY_LOWER, CANNY_UPPER = 0, 120
WINSIZE = 4

img = cv.imread("X:/cvImg/ma.jpg")
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

if SCALE_FLAG:
    img = cv.resize(img, (int(img.shape[1]* SCALE_FACTOR), int(img.shape[0]*SCALE_FACTOR)))

# Canny the image
imgCanny = cv.Canny(img, CANNY_LOWER, CANNY_UPPER)

cv.imwrite("edge.jpg", imgCanny)

gradder = hogger(imgCanny, WINSIZE, 2)


if DISP_FLAG:
    cv.imshow("canny", imgCanny)
    cv.waitKey(0)
    cv.destroyAllWindows()