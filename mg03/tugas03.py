from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# define constant variable
g = 9.8     # gravity acceleration
epsilon = 1e-3  # defined zero
t = [0]
dt = 1e-3
coef_e = 0.8     # restitution coefficient

# define function here
def glbb_hi(hi_1, vi, dt=1e-3):
    hi = hi_1 + vi * dt
    return hi
    
def glbb_vi(v1_1, a, dt=1e-3):
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
    if val < epsilon: return 1
    else: return 0


# define class here
class System():
    def __init__(self):
        self.energy = [0]   # total energy of system   

class Ball():
    def __init__(self, mass=1, pos=(0,0), velo=(0,0), acce=(0,0)):
        self.mass = mass
        self.pos = [pos]    # storing (x, y)
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


# main function
def run_tugas03():
    # initialize objects
    obj1 = Ball(mass=1, pos=(5,10), velo=(0,0), acce=(0,0))
    obj2 = Ball(mass=1, pos=(7,8), velo=(0,0), acce=(0,0))
    spring = Spring(k=50, length=3)

    # loop's stop condition
    flagWhile = check_zero(obj1.pos[-1][1]) and check_zero( abs(obj1.velo[-1][1]) ) \
                and check_zero(obj2.pos[-1][1]) and check_zero( abs(obj2.velo[-1][1]) )
    while not(flagWhile):
        print("in loop")
        # limit spring length, delta_l_max = 10%
        if ( (1-spring.tollerance)*spring.length[0] < spring.length[-1] < (1+spring.tollerance)*spring.length[0] ):
            v1_1 = (obj1.velo[-1][0], obj1.velo[-1][1])     # last 2nd --> v_{i-1}
            v2_1 = (obj2.velo[-1][0], obj2.velo[-1][1])
        else:
            v1_1 = (0, obj1.velo[-1][1])
            v2_1 = (0, obj2.velo[-1][1])

        # check if ball on ground & check if velocity < 0
        if (check_zero(obj1.pos[-1][1]) and check_zero(obj2.pos[-1][1])) \
                and obj1.velo[-1][1] < 0 and obj2.velo[-1][1] < 0:
            vx1 = glbb_vi(v1_1[0], obj1.acce[-1][0])
            vy1 = glbb_vi(v1_1[1], obj1.acce[-1][1]) * -coef_e
            (obj1.velo).append( (vx1, vy1) )
            vx2 = glbb_vi(v2_1[0], obj2.acce[-1][0])
            vy2 = glbb_vi(v2_1[1], obj2.acce[-1][1]) * -coef_e
            (obj2.velo).append( (vx2, vy2) )
            print("IF 1 (%s,%s) (%s,%s)" %(vx1,vy1,vx2,vy2))
        # check if obj1 on ground & check if velocity < 0
        elif (check_zero(obj1.pos[-1][1]) and obj1.velo[-1][1] < 0):
            vx1 = glbb_vi(v1_1[0], obj1.acce[-1][0])
            vy1 = glbb_vi(v1_1[1], obj1.acce[-1][1]) * -coef_e
            (obj1.velo).append( (vx1, vy1) )
            vx2 = glbb_vi(v2_1[0], obj2.acce[-1][0])
            vy2 = glbb_vi(v2_1[1], (-g+obj2.acce[-1][1]))
            (obj2.velo).append( (vx2, vy2) )
            print("IF 2 (%s,%s) (%s,%s)" %(vx1,vy1,vx2,vy2))
        # check if obj2 on ground & check if velocity < 0
        elif (check_zero(obj2.pos[-1][1]) and obj2.velo[-1][1] < 0):
            vx1 = glbb_vi(v1_1[0], obj1.acce[-1][0])
            vy1 = glbb_vi(v1_1[1], (-g+obj1.acce[-1][1]))
            (obj1.velo).append( (vx1, vy1) )
            vx2 = glbb_vi(v2_1[0], obj2.acce[-1][0])
            vy2 = glbb_vi(v2_1[1], obj2.acce[-1][1]) * -coef_e
            (obj2.velo).append( (vx2, vy2) )
            print("IF 3 (%s,%s) (%s,%s)" %(vx1,vy1,vx2,vy2))
        # if all obj in the air
        else:
            vx1 = glbb_vi(v1_1[0], obj1.acce[-1][0])
            vy1 = glbb_vi(v1_1[1], (-g+obj1.acce[-1][1]))
            (obj1.velo).append( (vx1, vy1) )
            vx2 = glbb_vi(v2_1[0], obj2.acce[-1][0])
            vy2 = glbb_vi(v2_1[1], (-g+obj2.acce[-1][1]))
            (obj2.velo).append( (vx2, vy2) )
            print("IF 4 (%s,%s) (%s,%s)" %(vx1,vy1,vx2,vy2))
        
        # update position
        x1 = glbb_hi(obj1.pos[-1][0], obj1.velo[-1][0])
        y1 = glbb_hi(obj1.pos[-1][1], obj1.velo[-1][1])
        (obj1.pos).append( (x1, y1) )
        x2 = glbb_hi(obj2.pos[-1][0], obj2.velo[-1][0])
        y2 = glbb_hi(obj2.pos[-1][1], obj2.velo[-1][1])
        (obj2.pos).append( (x2, y2) )

        # update length of spring
        L = eulclidian_dist(pos_1=(x1,y1), pos_2=(x2,y2))
        (spring.length).append(L)

        # update force caused by spring
        Fx1, Fy1 = spring.get_force_component(pos_1=(x1,y1), pos_2=(x2,y2))
        (spring.force).append( (Fx1, Fy1) )
        print("Fx, Fy = %s, %s" %(Fx1, Fy1))

        # update acceleration caused by spring. store it into Ball acceleration
        ax1, ay1 = spring.get_acce_component(m_obj=obj1.mass, pos_1=(x1,y1), pos_2=(x2,y2))
        ax2, ay2 = spring.get_acce_component(m_obj=obj2.mass, pos_1=(x1,y1), pos_2=(x2,y2))
        (obj1.acce).append( (Fx1, Fy1) )
        (obj2.acce).append( (-Fx1, -Fy1) )

        # update time
        t.append(t[-1] + dt)

    # plotting purposes
    arr_x1 = np.array( np.round(obj1.pos, decimals=2) )[:, 0]
    arr_y1 = np.array( np.round(obj1.pos, decimals=2) )[:, 1]
    arr_x2 = np.array( np.round(obj2.pos, decimals=2) )[:, 0]
    arr_y2 = np.array( np.round(obj2.pos, decimals=2) )[:, 1]

    fig = plt.figure()
    plt.ylim(0, 10)
    plt.xlim(0, 6)
    def animate(i):
        lines = plt.plot([arr_x1[i], arr_x2[i]],
                        [arr_y1[i], arr_y2[i]], 'ok-')
        return lines

    ani = animation.FuncAnimation(fig, animate, len(arr_x1), interval=dt/1e3, blit=True)
    plt.show()


# other method
def run_tugas03a():
    # initialize objects
    obj1 = Ball(mass=1, pos=(5,10), velo=(0,0), acce=(0,0))
    obj2 = Ball(mass=1, pos=(7,8), velo=(0,0), acce=(0,0))
    spring = Spring(k=50, length=3)

    # loop's stop condition
    flagWhile = check_zero(obj1.pos[-1][1]) and check_zero( abs(obj1.velo[-1][1]) ) \
                and check_zero(obj2.pos[-1][1]) and check_zero( abs(obj2.velo[-1][1]) )
    while not(flagWhile):
        print("in loop")
        # limit spring length, delta_l_max = 10%
        if ( (1-spring.tollerance)*spring.length[0] < spring.length[-1] < (1+spring.tollerance)*spring.length[0] ):
            v1_1 = (obj1.velo[-1][0], obj1.velo[-1][1])     # last 2nd --> v_{i-1}
            v2_1 = (obj2.velo[-1][0], obj2.velo[-1][1])
        else:
            v1_1 = (0, obj1.velo[-1][1])
            v2_1 = (0, obj2.velo[-1][1])

        # check if ball on ground & check if velocity < 0
        if (check_zero(obj1.pos[-1][1]) and check_zero(obj2.pos[-1][1])) \
                and obj1.velo[-1][1] < 0 and obj2.velo[-1][1] < 0:
            vx1 = glbb_vi(v1_1[0], obj1.acce[-1][0])
            vy1 = glbb_vi(v1_1[1], obj1.acce[-1][1]) * -coef_e
            (obj1.velo).append( (vx1, vy1) )
            vx2 = glbb_vi(v2_1[0], obj2.acce[-1][0])
            vy2 = glbb_vi(v2_1[1], obj2.acce[-1][1]) * -coef_e
            (obj2.velo).append( (vx2, vy2) )
            print("IF 1 (%s,%s) (%s,%s)" %(vx1,vy1,vx2,vy2))
        # check if obj1 on ground & check if velocity < 0
        elif (check_zero(obj1.pos[-1][1]) and obj1.velo[-1][1] < 0):
            vx1 = glbb_vi(v1_1[0], obj1.acce[-1][0])
            vy1 = glbb_vi(v1_1[1], obj1.acce[-1][1]) * -coef_e
            (obj1.velo).append( (vx1, vy1) )
            vx2 = glbb_vi(v2_1[0], obj2.acce[-1][0])
            vy2 = glbb_vi(v2_1[1], (-g+obj2.acce[-1][1]))
            (obj2.velo).append( (vx2, vy2) )
            print("IF 2 (%s,%s) (%s,%s)" %(vx1,vy1,vx2,vy2))
        # check if obj2 on ground & check if velocity < 0
        elif (check_zero(obj2.pos[-1][1]) and obj2.velo[-1][1] < 0):
            vx1 = glbb_vi(v1_1[0], obj1.acce[-1][0])
            vy1 = glbb_vi(v1_1[1], (-g+obj1.acce[-1][1]))
            (obj1.velo).append( (vx1, vy1) )
            vx2 = glbb_vi(v2_1[0], obj2.acce[-1][0])
            vy2 = glbb_vi(v2_1[1], obj2.acce[-1][1]) * -coef_e
            (obj2.velo).append( (vx2, vy2) )
            print("IF 3 (%s,%s) (%s,%s)" %(vx1,vy1,vx2,vy2))
        # if all obj in the air
        else:
            vx1 = glbb_vi(v1_1[0], obj1.acce[-1][0])
            vy1 = glbb_vi(v1_1[1], (-g+obj1.acce[-1][1]))
            (obj1.velo).append( (vx1, vy1) )
            vx2 = glbb_vi(v2_1[0], obj2.acce[-1][0])
            vy2 = glbb_vi(v2_1[1], (-g+obj2.acce[-1][1]))
            (obj2.velo).append( (vx2, vy2) )
            print("IF 4 (%s,%s) (%s,%s)" %(vx1,vy1,vx2,vy2))
        
        # update position
        x1 = glbb_hi(obj1.pos[-1][0], obj1.velo[-1][0])
        y1 = glbb_hi(obj1.pos[-1][1], obj1.velo[-1][1])
        (obj1.pos).append( (x1, y1) )
        x2 = glbb_hi(obj2.pos[-1][0], obj2.velo[-1][0])
        y2 = glbb_hi(obj2.pos[-1][1], obj2.velo[-1][1])
        (obj2.pos).append( (x2, y2) )

        # update length of spring
        L = eulclidian_dist(pos_1=(x1,y1), pos_2=(x2,y2))
        (spring.length).append(L)

        # update force caused by spring
        Fx1, Fy1 = spring.get_force_component(pos_1=(x1,y1), pos_2=(x2,y2))
        (spring.force).append( (Fx1, Fy1) )
        print("Fx, Fy = %s, %s" %(Fx1, Fy1))

        # update acceleration caused by spring. store it into Ball acceleration
        ax1, ay1 = spring.get_acce_component(m_obj=obj1.mass, pos_1=(x1,y1), pos_2=(x2,y2))
        ax2, ay2 = spring.get_acce_component(m_obj=obj2.mass, pos_1=(x1,y1), pos_2=(x2,y2))
        (obj1.acce).append( (Fx1, Fy1) )
        (obj2.acce).append( (-Fx1, -Fy1) )

        # update time
        t.append(t[-1] + dt)

    # plotting purposes
    arr_x1 = np.array( np.round(obj1.pos, decimals=2) )[:, 0]
    arr_y1 = np.array( np.round(obj1.pos, decimals=2) )[:, 1]
    arr_x2 = np.array( np.round(obj2.pos, decimals=2) )[:, 0]
    arr_y2 = np.array( np.round(obj2.pos, decimals=2) )[:, 1]

    fig = plt.figure()
    plt.ylim(0, 10)
    plt.xlim(0, 6)
    def animate(i):
        lines = plt.plot([arr_x1[i], arr_x2[i]],
                        [arr_y1[i], arr_y2[i]], 'ok-')
        return lines

    ani = animation.FuncAnimation(fig, animate, len(arr_x1), interval=dt/1e3, blit=True)
    plt.show()


if __name__ == "__main__":
    run_tugas03a()