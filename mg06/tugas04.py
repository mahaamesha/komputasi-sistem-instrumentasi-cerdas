import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

def cvt_gray(frame, c_bgr=(0.114, 0.587, 0.299)):
    # create black img that have similar size to img
    w,h,c = frame.shape
    gray = np.zeros( (w,h,c) )

    # extract 3 channel: bgr
    ch_b, ch_g, ch_r = frame[:,:,0], frame[:,:,1], frame[:,:,2]

    # convert bgr channel to gray
    for i in range(w):
        for j in range(h):
            gray[i][j]  = c_bgr[0] * ch_b[i][j] \
                            + c_bgr[1] * ch_g[i][j] \
                            + c_bgr[2] * ch_r[i][j]
    
    return gray


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
    # path_arr = ["cubic_puzzle.jpg"]
    for i in range(len(path_arr)):
        path_arr[i] = os.path.join(folder_path, path_arr[i])
        print(path_arr[i])
        run_tugas04(path_arr[i])