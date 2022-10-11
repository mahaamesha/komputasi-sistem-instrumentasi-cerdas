from cv2 import getTickCount, getTickFrequency

# define class to store data
class Data():
    def __init__(self):
        self.fps = None
        self.time = [None,None] # store time start & end when in oscilataion
        self.period = None
        self.mass = None
        self.pos = [(None,None)]    # storing (x, y)
        self.velo = [(None,None)]   # storing (vx, vy)
        self.acce = [(None,None)]   # storing (ax, ay)
        # self.ep = [mass * g * pos[1]]   # storing mgh
        # self.ek = [1/2 * mass * magnitude(velo[0], velo[1])**2]     # storing 1/2 m v^2
        # self.em = [self.ep + self.ek]   # storing em of a ball
    
    def store_fps(self, fps):
        if self.fps == None:
            self.fps = fps
            print("FPS = %s." %fps)
    
    def store_centroid(self, centroid):
        if self.pos[0] == (None,None):  # store initial value
            self.pos[0] = centroid
            (self.pos).append( (None,None) )    # i only need to store 2 centroid data
        else:
            self.pos[1] = centroid
        print("(cx,cy) = (%s,%s)" %(centroid[0], centroid[1]))
    
    def store_period(self):
        if self.pos[1] == (None,None):
            self.time[0] = getTickCount()
        
        # store period when in peak
        if self.pos[1] == self.pos[0]:
            self.time[1] = getTickCount()
            self.period = (self.time[1] - self.time[0]) / getTickFrequency()
            print("T = %s sekon" %self.period)
            

