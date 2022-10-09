import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

def cvt_gray(img, c_bgr=(0.114, 0.587, 0.299)):
    # create black img that have similar size to img
    w,h,c = img.shape
    img_gray = np.zeros( (w,h,c) )

    # extract 3 channel: bgr
    img_b, img_g, img_r = img[:,:,0], img[:,:,1], img[:,:,2]

    # convert bgr channel to gray
    for i in range(w):
        for j in range(h):
            img_gray[i][j]  = c_bgr[0] * img_b[i][j] \
                            + c_bgr[1] * img_g[i][j] \
                            + c_bgr[2] * img_r[i][j]
    
    return img_gray

    

    
    

def convert_gray(source_bgr=[], coef_bgr=(0.114, 0.587, 0.299)):
    pixel_map = source_bgr[0].load()
    h,w = source_bgr[0].shape
    gray = np.zeros([h,w])
    for i in range(h):
        for j in range(w):
            r, g, b, p = source_bgr[0].getpixel((i, j))
            gray = coef_bgr[0] * (source_bgr[0])[i][j] \
                        + coef_bgr[1] * (source_bgr[1])[i][j] \
                        + coef_bgr[2] * (source_bgr[2])[i][j]
            gray[i][j] = int( gray[i][j] )
    return gray


def extract_color(frame, lower=[0,200,200], upper=[20,255,255]):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower = np.array(lower)
    upper = np.array(upper)

    mask = cv.inRange(hsv, lower, upper)
    res = cv.bitwise_and(frame,frame, mask=mask)
    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    return res


def run_tugas04(path="mg06/cubic_puzzle.jpg"):
    # read img in rgb color space
    img = cv.imread(path)
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    gray2 = cvt_gray(img)

    # show image
    cv.imshow("Original", img)
    cv.imshow("Gray", gray)
    cv.imshow("Gray2", gray2)
    # cv.imshow("Extracted Color", extraced_color)

    cv.waitKey(0)
    cv.destroyAllWindows()
    print("Done")

if __name__ == "__main__":
    folder_path = "mg06/"
    path_arr = ["cubic_puzzle.jpg",
                "red_sample.jpg",
                "green_sample.jpg",
                "blue_sample.jpg"]
    path_arr = ["cubic_puzzle.jpg"]
    for i in range(len(path_arr)):
        path_arr[i] = os.path.join(folder_path, path_arr[i])
        print(path_arr[i])
        run_tugas04(path_arr[i])