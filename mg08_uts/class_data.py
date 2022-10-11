from cv2 import getTickCount, getTickFrequency

# define class to store data
class Data():
    def __init__(self):
        self.fps = None
        self.time = [None,None] # store time start & end when in oscilataion
        self.period = None
        self.pos = [(None,None)]    # storing centroid (cx, cy)
    
    def store_fps(self, fps):
        if self.fps != fps:
            self.fps = fps
            print("FPS = %s." %fps)
    
    def store_area(self, area):
        self.area = area
    
    def store_centroid(self, centroid):
        if self.pos[0] == (None,None):  # store initial value
            self.pos[0] = centroid
            (self.pos).append( (None,None) )    # i only need to store 2 centroid data
        else:
            self.pos[1] = centroid
        print("centroid = [%s,%s]" %(self.pos[0], self.pos[1]))
    
    def store_period(self):
        if self.time[0] == None:
            self.time[0] = getTickCount()
        # store period when in peak
        elif self.pos[1] == self.pos[0]:
            self.time[1] = getTickCount()
            self.period = (self.time[1] - self.time[0]) / getTickFrequency()
            print("T = %s sekon" %self.period)
            self.time[0] = None     # so that make it go back to first condition
        print("time     = [%s,%s]" %(self.time[0], self.time[1]))
        