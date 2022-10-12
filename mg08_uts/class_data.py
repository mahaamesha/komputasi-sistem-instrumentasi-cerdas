from cv2 import getTickCount, getTickFrequency
from math import sqrt, pi

# define class to store data
class Data():
    def __init__(self):
        self.fps = None
        self.time = [None,None] # store time start & end when in oscilataion
        self.period = None
        self.period_theory = None
        self.period_err = None
        self.pos = [(None,None)]    # storing centroid (cx, cy)
        self.area = [None,None]
    
    def store_fps(self, fps):
        if self.fps != fps:
            self.fps = fps
            print("FPS = %s." %fps)
    
    def store_area(self, area):
        if self.area[0] == None:
            self.area[0] = area
        else:
            self.area[1] = area
        print("Area = [%s]" %area)
    
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
    
    def store_period_theory(self, L=1, g=9.8):
        if self.period_theory == None:  # only do this below, once
            T = 2*pi * sqrt(L/g)
            self.period_theory = float( "{:.5f}".format(T) )
    
    def store_period_err(self):
        if self.period != None:
            err = abs(self.period - self.period_theory) / self.period_theory * 100
            self.period_err = float( "{:.3f}".format(err) )

