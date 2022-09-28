from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

g = 9.8     # gravity acceleration
epsilon = 1e-3  # defined zero
t = [0]
dt = 1e-2
coef_e = 0.8     # restitution coefficient

def glbb_hi(hi_1, vi, dt=dt):
    hi = hi_1 - vi * dt
    return hi
    
def glbb_vi(v1_1, a, dt=dt):
    vi = v1_1 + a * dt
    return vi

def energy_potential(m, g=10, h=0):
    return m * g * h

def energy_kinetic(m, v):
    return 1/2 * m * v**2

def eulclidian_dist(pos_1=(0,0), pos_2=(0,0)):   # pos is tuple (x,y)
    delta_x = pos_2[0] - pos_1[0]
    delta_y = pos_2[1] - pos_1[1]
    dist = sqrt(delta_x**2 + delta_y**2)
    return dist

def get_cos_sin(val, pos_1=(0,0), pos_2=(0,0)):
    # teta form horizontal line
    delta_x = pos_2[0] - pos_1[0]
    delta_y = pos_2[1] - pos_1[1]
    cos_teta = delta_x / val
    sin_teta = delta_y / val
    return cos_teta, sin_teta

def magnitude(x, y):
    return sqrt(x**2 + y**2)

def check_zero(val, epsilon=1e-3):
    if val <= epsilon: return 1
    else: return 0



class System():
    def __init__(self):
        self.energy = [0]    # total energy of system   

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
    def __init__(self, k=1e3, length=1, force=(0,0)):
        self.k = k
        self.length = [length]
        self.tollerance = 10/100    # 10%
        self.force = [force]    # storing (Fx, Fy)
        self.work = self.calc_work()

    def calc_force(self):
        delta_l = self.length[-1] - self.length[0]      # (last - initial) length
        f = self.k * delta_l
        return f
    
    def get_force_component(self, pos_1=(0,0), pos_2=(0,0)):
        cos_teta, sin_teta = get_cos_sin(self.length[-1], pos_1, pos_2)
        fx = self.calc_force() * cos_teta
        fy = self.calc_force() * sin_teta
        return fx, fy
    
    def get_acce_component(self, m_obj=0, pos_1=(0,0), pos_2=(0,0)):
        cos_teta, sin_teta = get_cos_sin(self.length[-1], pos_1, pos_2)
        ax = self.k / m_obj * self.length[-1] * cos_teta
        ay = self.k / m_obj * self.length[-1] * sin_teta
        return ax, ay

    def calc_work(self):
        delta_l = self.length[-1] - self.length[0]      # (last - initial) length
        w = 1/2 * self.k * delta_l**2       # work = 1/2 k delta_l^2
        return w


def run_main():
    # initialize objects
    obj1 = Ball(mass=1, pos=(1,3), velo=(0,0), acce=(0,0))
    obj2 = Ball(mass=1, pos=(3,5), velo=(0,0), acce=(0,0))
    spring = Spring(k=1e2, length=3)

    # loop's stop condition
    flagWhile = check_zero(obj1.pos[-1][1]) and check_zero( abs(obj1.velo[-1][1]) ) \
                and check_zero(obj2.pos[-1][1]) and check_zero( abs(obj2.velo[-1][1]) )
    while not(flagWhile):
        print("in loop", obj1.pos)
        # limit spring length, delta_l_max = 10%
        if ( (1-spring.tollerance)*spring.length[0] < spring.length[-1] < (1+spring.tollerance)*spring.length[0] ):
            v1_1 = (obj1.velo[-1][0], obj1.velo[-1][1])     # last 2nd --> v_{i-1}
            v2_1 = (obj)

        # check if ball on ground & check if velocity < 0
        if (check_zero(obj1.pos[-1][1]) and check_zero(obj2.pos[-1][1])) \
            and obj1.velo[-1][1] < 0 and obj2.velo[-1][1] < 0:
            vx1 = glbb_vi(obj1.velo[-1][0], obj1.acce[-1][0])
            vy1 = -coef_e * glbb_vi(obj1.velo[-1][1], obj1.acce[-1][1])
            (obj1.velo).append( (vx1, vy1) )
            vx2 = glbb_vi(obj2.velo[-1][0], obj2.acce[-1][0])
            vy2 = -coef_e * glbb_vi(obj2.velo[-1][1], obj2.acce[-1][1])
            (obj2.velo).append( (vx2, vy2) )
        # check if obj1 on ground & check if velocity < 0
        elif (check_zero(obj1.pos[-1][1]) and obj1.velo[-1][1] < 0):
            vx1 = glbb_vi(obj1.velo[-1][0], obj1.acce[-1][0])
            vy1 = -coef_e * glbb_vi(obj1.velo[-1][1], obj1.acce[-1][1])
            (obj1.velo).append( (vx1, vy1) )
            vx2 = glbb_vi(obj2.velo[-1][0], obj2.acce[-1][0])
            vy2 = glbb_vi(obj2.velo[-1][1], -g+obj2.acce[-1][1])
            (obj2.velo).append( (vx2, vy2) )
        # check if obj2 on ground & check if velocity < 0
        elif (check_zero(obj2.pos[-1][1]) and obj2.velo[-1][1] < 0):
            vx1 = glbb_vi(obj1.velo[-1][0], obj1.acce[-1][0])
            vy1 = glbb_vi(obj1.velo[-1][1], -g+obj1.acce[-1][1])
            (obj1.velo).append( (vx1, vy1) )
            vx2 = glbb_vi(obj2.velo[-1][0], obj2.acce[-1][0])
            vy2 = -coef_e * glbb_vi(obj2.velo[-1][1], -g+obj2.acce[-1][1])
            (obj2.velo).append( (vx2, vy2) )
        # if all obj in the air
        else:
            vx1 = glbb_vi(obj1.velo[-1][0], obj1.acce[-1][0])
            vy1 = glbb_vi(obj1.velo[-1][1], -g+obj1.acce[-1][1])
            (obj1.velo).append( (vx1, vy1) )
            vx2 = glbb_vi(obj2.velo[-1][0], obj2.acce[-1][0])
            vy2 = glbb_vi(obj2.velo[-1][1], -g+obj2.acce[-1][1])
            (obj2.velo).append( (vx2, vy2) )
        
        # update position
        x1 = glbb_hi(obj1.pos[-1][0], obj1.acce[-1][0])
        y1 = glbb_hi(obj1.pos[-1][1], obj1.acce[-1][1])
        (obj1.pos).append( (x1, y1) )
        x2 = glbb_hi(obj2.pos[-1][0], obj2.acce[-1][0])
        y2 = glbb_hi(obj2.pos[-1][1], obj2.acce[-1][1])
        (obj2.pos).append( (x2, y2) )

        # update length of spring
        L = eulclidian_dist(pos_1=(x1,y1), pos_2=(x2,y2))
        (spring.length).append(L)

        # update force caused by spring
        Fx, Fy = spring.get_force_component(pos_1=(x1,y1), pos_2=(x2,y2))
        (spring.force).append( (Fx, Fy) )

        # update acceleration caused by spring. store it into Ball acceleration
        ax1, ay1 = spring.get_acce_component(m_obj=obj1.mass, pos_1=(x1,y1), pos_2=(x2,y2))
        ax2, ay2 = spring.get_acce_component(m_obj=obj2.mass, pos_1=(x1,y1), pos_2=(x2,y2))
        (obj1.acce).append( (ax1, ay1) )
        (obj2.acce).append( (ax2, ay2) )

        # update time
        t.append(t[-1] + dt)

    # plotting purposes
    arr_x1 = np.array(obj1.pos)[:, 0]
    arr_y1 = np.array(obj1.pos)[:, 1]
    arr_x2 = np.array(obj2.pos)[:, 0]
    arr_y2 = np.array(obj2.pos)[:, 1]
    
    fig = plt.figure()
    def animate(i):
        lines = plt.plot([arr_x1, arr_x2],
                        [arr_y1, arr_y2])
        return lines

    ani = animation.FuncAnimation(fig, animate, len(t), interval=dt, blit=True)
    plt.show()








    # while obj1.pos[-1][1] > epsilon or abs(obj1.velo[-1][1]) > epsilon \
    #         or obj2.pos[-1][1] > epsilon or abs(obj2.velo[-1][1]) > epsilon:
    #     # update velocity in x direction
    #     vx1 = glbb_vi(v1_1=obj1.velo[-1][0], a=obj1.acce[-1][0])
    #     vx2 = glbb_vi(v1_1=obj2.velo[-1][0], a=obj2.acce[-1][0])

    #     # update velocity in y direction
    #     if check_zero(obj1.pos[-1][1]) and check_zero(obj1.velo[-1][1]):
    #         vy1 = -coef_e * glbb_vi(v1_1=obj1.velo[-1][1], a=obj1.acce[-1][1])
    #     else:
    #         ay1 = -g + obj1.acce[-1][1]
    #         vy1 = -coef_e * glbb_vi(v1_1=obj1.velo[-1][1], a=ay1)
        
    #     if check_zero(obj1.pos[-1][1]) and check_zero(obj1.velo[-1][1]):
    #         vy1 = -coef_e * glbb_vi(v1_1=obj1.velo[-1][1], a=obj1.acce[-1][1])
    #     else:
    #         ay2 = -g + obj1.acce[-1][1]
    #         vy1 = -coef_e * glbb_vi(v1_1=obj1.velo[-1][1], a=ay2)
        
    #     # update position
    #     x1 = glbb_hi()

    #     (obj1.velo).append()


def run_main2():
    pass


    # print( obj1.check_zero(obj1.pos, epsilon))

    # check if system is not yet in equilibrium state
    # while 
# cek apakah setiap bola mencapai lantai
# hitung posisi, velocity dengan glbb (untuk setiap bola)
# hitung percepatan dengan hk 2 newton (untuk setiap bola)
# dari posisi 2 bola, hitung panjang pegas

if __name__ == "__main__":
    run_main()