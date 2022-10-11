import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os


def cvt_gray(img, c_bgr=(0.114, 0.587, 0.299)):
    # create black img that have similar size to img
    w,h,c = img.shape
    img_gray = np.zeros( (w,h) )
    
    # extract 3 channel: bgr
    img_b, img_g, img_r = img[:,:,0], img[:,:,1], img[:,:,2]
    
    # convert bgr channel to gray
    for i in range(w):
        for j in range(h):
            img_gray[i,j]   = c_bgr[0] * img_b[i,j] \
                            + c_bgr[1] * img_g[i,j] \
                            + c_bgr[2] * img_r[i,j]
    return img_gray


def run_tugas04(path="mg06/cubic_puzzle.jpg"):
    # read img in rgb color space
    img = cv.imread(path)
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    print("Original")
    plt.imshow(img_rgb, cmap="gray")
    plt.show()
    
    # gray image
    c_bgr = (0.114, 0.587, 0.299)
    img_gray = cvt_gray(img, c_bgr)
    print("Grayscale")
    plt.imshow(img_gray, cmap="gray")
    plt.show()
    
    # compare every channel intensity
    print("Compare BGR Intensity")
    plt.subplots(nrows=1, ncols=3, tight_layout=1)
    plt.subplot(1,3,1); plt.imshow(img[:,:,0], cmap="gray"); plt.title("B Intensity"); plt.colorbar(orientation="horizontal")
    plt.subplot(1,3,2); plt.imshow(img[:,:,1], cmap="gray"); plt.title("G Intensity"); plt.colorbar(orientation="horizontal")
    plt.subplot(1,3,3); plt.imshow(img[:,:,2], cmap="gray"); plt.title("R Intensity"); plt.colorbar(orientation="horizontal")
    plt.show()

    print("Done")


if __name__ == "__main__":
    folder_path = "./"
    path_arr = ["cubic_puzzle.jpg",
                "red_sample.jpg",
                "green_sample.jpg",
                "blue_sample.jpg"]
    # path_arr = ["cubic_puzzle.jpg"]
    for i in range(len(path_arr)):
        print("path: %s" %path_arr[i])
        path_arr[i] = os.path.join(folder_path, path_arr[i])
        run_tugas04(path_arr[i])
        print("\n")