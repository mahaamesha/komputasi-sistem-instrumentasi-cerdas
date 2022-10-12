import cv2 as cv
import numpy as np
from imutils import grab_contours
from class_data import Data

myData = Data()


def convert_gray(img, c_bgr=(0.114, 0.587, 0.299)):
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


def extract_color(frame, lower=[0,0,0], upper=[0,0,0]):
    # convert BGR to HSV color space
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # get masking frame in 1/0 intensity
    lower, upper = np.array(lower), np.array(upper)
    mask = cv.inRange(hsv, lower, upper)

    # extract frame using masking
    res = cv.bitwise_and(frame, frame, mask=mask)

    return res, mask


def get_area(cnts):
    arr = []    # store area of every contour
    for cnt in cnts:
        area = cv.contourArea(cnt)
        arr.append(area)
    return area


def draw_min_rectangle(frame, cnts):
    arr = []    # store arr of box for every contour detected
    for cnt in cnts:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        arr.append(box)
    
    for (a,b,c,d) in arr:
        cv.line(frame, pt1=a, pt2=b, color=(0,255,0), thickness=2)
        cv.line(frame, pt1=b, pt2=c, color=(0,255,0), thickness=2)
        cv.line(frame, pt1=c, pt2=d, color=(0,255,0), thickness=2)
        cv.line(frame, pt1=d, pt2=a, color=(0,255,0), thickness=2)

    return frame, arr


# get centroid of every detected cnt, return it as array
def draw_centroid(frame, cnts):
    arr = []    # store centroid of multiple objects
    # get the centroid
    for cnt in cnts:
        M = cv.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        arr.append( (cx,cy) )
    
    # draw centroid
    for (cx,cy) in arr:
        cv.circle(frame, center=(cx,cy), radius=3, color=(0,255,0), thickness=-1)

    return frame, arr


def put_text2frame(frame, label, num, count, factor=1):     # count: number of line(s)
    text = ""
    org = (20*factor, 30*factor)
    dist = 20*factor
    fontFace = cv.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5*factor
    color = (0,0,0)
    thickness = 1*factor
    text_color_bg = (255,255,255)

    text = str("%s: %s" %(label, num))
    temp_org = (org[0], org[1]+dist*count)     # 20 is distance to new line

    # background
    text_size, _ = cv.getTextSize(text, fontFace, fontScale, thickness)
    text_w, text_h = text_size
    cv.rectangle(frame, temp_org, (temp_org[0]+text_w, temp_org[1]-text_h), text_color_bg, -1)

    # draw text
    cv.putText(frame, text, temp_org, fontFace, fontScale, color, thickness, cv.LINE_AA)

    return frame


def process_func(frame):
    # extract specific color range
    extracted, mask = extract_color(frame, lower=[0,127,127], upper=[179,255,255])

    # remove noise & strengthen the region
    kernel = np.ones( (3,3), np.uint8 )
    erodila = cv.erode(mask, kernel, iterations=2)
    erodila = cv.dilate(erodila, kernel, iterations=3)

    # find & draw contour
    cnts = cv.findContours(erodila, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = grab_contours(cnts)
    # contoured = cv.drawContours(frame, cnts, -1, (0,255,0), 3)
    
    area = get_area(cnts)
    centroid_frame, box = draw_min_rectangle(frame, cnts)
    centroid_frame, centroid = draw_centroid(frame, cnts)
    myData.store_centroid(centroid[0])  # centroid[0] because the array store centroid of many objects
    myData.store_area(area)
    myData.store_period_theory()
    myData.store_period()
    myData.store_period_err()

    return centroid_frame


def get_cap_size(cap):
    width = int( cap.get(cv.CAP_PROP_FRAME_WIDTH) )
    heigth = int( cap.get(cv.CAP_PROP_FRAME_HEIGHT) )
    return width, heigth


# to reverse frame, so every frame will be contiuous
def reverse_playback(cap, frame_counter):
    frame_counter += 1

    if frame_counter == cap.get(cv.CAP_PROP_FRAME_COUNT):
        frame_counter = 0
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    
    return cap, frame_counter


def play_video(path, isSave=0, isLoop=1):
    cap = cv.VideoCapture(path)
    cap_width, cap_heigth = get_cap_size(cap)

    # for saving, I need define codec and create VideoWriter object
    if isSave:
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        out = cv.VideoWriter("mg08_uts/result.mp4", fourcc, 20.0, (cap_width,cap_heigth))

    if (not cap.isOpened()):
        print("Error: Can't open camera")
        exit()

    frame_counter = 0       # used in reverse_playback()
    while True:
        # capture frame-by-frame
        ret, frame = cap.read()

        # if frame is read correctly, ret is True
        if (not ret):
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # playback video by reset the frame_counter
        if isLoop:
            cap, frame_counter = reverse_playback(cap, frame_counter)
        
        # image processing for every frame
        frame = process_func(frame)
        # adding text: fps, contouqqqrs, etc
        fps = cap.get(cv.CAP_PROP_FPS)
        myData.store_fps(fps)   # store data to class

        # put text to frame
        frame = put_text2frame(frame, "FPS", myData.fps, 0)
        frame = put_text2frame(frame, "(cx,cy)", myData.pos[1], 1)
        frame = put_text2frame(frame, "A", myData.area, 2)
        frame = put_text2frame(frame, "T", myData.period, 3)
        frame = put_text2frame(frame, "T_teori", myData.period_theory, 4)
        frame = put_text2frame(frame, "%T", myData.period_err, 5)
        

        # write final frame
        if isSave: out.write(frame)

        # show the frame
        cv.imshow("frame", frame)

        # exit the window
        if (cv.waitKey(1) == ord('q')):
            break

        cv.waitKey(10)
    
    cap.release()
    if isSave: out.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    path = "mg08_uts/bandul.mp4"
    play_video(path=path, isSave=1, isLoop=1)