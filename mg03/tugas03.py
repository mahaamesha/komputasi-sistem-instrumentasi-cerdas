from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.animation as ani

g = 9.8     # gravity acceleration
epsilon = 1e-3  # defined zero
t = [0]
dt = 1e-2

def calc_hi(hi_1, vi, dt):
    hi = hi_1 - vi * dt
    return hi

def calc_vi(v1_1, g, dt):
    vi = v1_1 + g * dt
    return vi

def magnitude(x, y):
    return sqrt(x**2 + y**2)

def energy_potential(m, g=10, h=0):
    return m * g * h

def energy_kinetic(m, v):
    return 1/2 * m * v**2

def check_zero(val, epsilon=1e-3):
    if val <= epsilon: return 1
    else: return 0



class System():
    def __init__(self):
        self.energy = []    # total energy of system   

class Ball():
    def __init__(self, mass=1, pos=(0,0), velo=(0,0), acce=(0,0)):
        self.mass = mass
        self.pos = [pos]    # storing (x,y)
        self.velo = [velo]  # storing (vx, vy)
        self.acce = [acce]  # storing (ax, ay)
        self.ep = [mass * g * pos[1]]   # storing mgh
        self.ek = [1/2 * mass * magnitude(velo[0], velo[1])**2]     # storing 1/2 m v^2
        self.em = [self.ep + self.ek]   # storing em of a ball

class Spring():
    def __init__(self, k=1e3, length=1, force=0):
        self.k = k
        self.length = [length]
        self.force = force
        self.work = self.cals_spring_work()

    # def calc_force(self, last_pos_1=(0,0), last_pos_2=(0,0)):
    #     return

    def calc_work(self):
        delta_l = self.length[-1] - self.length[0]      # (last - initial) length
        w = 1/2 * self.k * delta_l**2       # work = 1/2 k delta_l^2
        return w



def euler_dist(pos_1, pos_2):   # pos is tuple (x,y)
    delta_x = pos_2[0] - pos_1[0]
    delta_y = pos_2[1] - pos_1[1]
    dist = sqrt(delta_x**2 + delta_y**2)
    return dist


def run_main():
    # initialize objects
    obj1 = Ball(mass=1, pos=(5,1), velo=(0,0), acce=(0,0))
    obj2 = Ball(mass=1, pos=(5,5), velo=(0,0), acce=(0,0))

    # every object not stop yet
    flagWhile = check_zero(obj1.pos[-1][1]) and check_zero(obj1.velo[-1][1]) \
                and obj2.check_zero(obj2.pos[-1][1]) and obj2.check_zero(obj2.velo[-1][1])
    while flagWhile:
        obj1.pos[-1][1] -= 1


    # print( obj1.check_zero(obj1.pos, epsilon))

    # check if system is not yet in equilibrium state
    # while 
# cek apakah setiap bola mencapai lantai
# hitung posisi, velocity dengan glbb (untuk setiap bola)
# hitung percepatan dengan hk 2 newton (untuk setiap bola)
# dari posisi 2 bola, hitung panjang pegas

if __name__ == "__main__":
    run_main()