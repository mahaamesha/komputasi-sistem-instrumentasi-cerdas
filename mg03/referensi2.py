import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

t = [0]
epsilon = 1e-3
epsilon_v = 1e-2
dt = 1e-3
L = 3
k = 50
g = 9.8
r_1 = [[5, 10]]
r_2 = [[7, 8]]
v_1 = [[0, 0]]
v_2 = [[0, 0]]
a_1 = [[0, 0]]
a_2 = [[0, 0]]
L = [np.sqrt((r_1[0][0]-r_2[0][0])**2 + (r_1[0][1] - r_2[0][1])**2)]

while not(abs(v_1[-1][1]) < epsilon_v and r_1[-1][1] < epsilon \
          and abs(v_2[-1][1]) < epsilon_v and r_2[-1][1] < epsilon):
    if (0.9 * L[0] < L[-1] < 1.1 * L[0]):
        v_1_old = [v_1[-1][0], v_1[-1][1]]
        v_2_old = [v_2[-1][0], v_2[-1][1]]
    else:
        v_1_old = [0, v_1[-1][1]]
        v_2_old = [0, v_2[-1][1]]
        
    if (r_1[-1][1] < epsilon and r_2[-1][1] < epsilon \
        and v_1[-1][1] < 0 and v_2[-1][1] < 0):
        v_1.append([v_1_old[0] + a_1[-1][0]*dt, -0.8 * (v_1_old[1] + a_1[-1][1]*dt)])
        v_2.append([v_2_old[0] + a_2[-1][0]*dt, -0.8 * (v_2_old[1] + a_2[-1][1]*dt)])
    elif (r_1[-1][1] < epsilon and v_1[-1][1] < 0):
        v_1.append([v_1_old[0] + a_1[-1][0]*dt, -0.8 * (v_1_old[1] + a_1[-1][1]*dt)])
        v_2.append([v_2_old[0] + a_2[-1][0]*dt, v_2_old[1] + (-g + a_2[-1][1])*dt])
    elif (r_2[-1][1] < epsilon and v_2[-1][1] < 0):
        v_1.append([v_1_old[0] + a_1[-1][0]*dt, v_1_old[1] + (-g + a_1[-1][1])*dt])
        v_2.append([v_2_old[0] + a_2[-1][0]*dt, -0.8 * (v_2_old[1] + a_2[-1][1]*dt)])
    else:
        v_1.append([v_1_old[0] + a_1[-1][0]*dt, v_1_old[1] + (-g + a_1[-1][1])*dt])
        v_2.append([v_2_old[0] + a_2[-1][0]*dt, v_2_old[1] + (-g + a_2[-1][1])*dt])
    r_1.append([r_1[-1][0]+v_1[-1][0]*dt, r_1[-1][1]+v_1[-1][1]*dt])
    r_2.append([r_2[-1][0]+v_2[-1][0]*dt, r_2[-1][1]+v_2[-1][1]*dt])
    L.append(np.sqrt((r_1[-1][0]-r_2[-1][0])**2 + (r_1[-1][1] - r_2[-1][1])**2))
    F = k*(L[-1] - L[0])
    F_1 = [F*(r_2[-1][0]-r_1[-1][0])/L[-1], F*(r_2[-1][1]-r_1[-1][1])/L[-1]]
    F_2 = [-1*F*(r_2[-1][0]-r_1[-1][0])/L[-1], -1*F*(r_2[-1][1]-r_1[-1][1])/L[-1]]
    a_1.append([F_1[0], F_1[1]])
    a_2.append([F_2[0], F_2[1]])
    t.append(t[-1]+dt)

r_1_np, r_2_np = np.array(r_1), np.array(r_2)
x_1, y_1 = r_1_np[:,0], r_1_np[:,1]
x_2, y_2 = r_2_np[:,0], r_2_np[:,1]
print(min(L), max(L))
fig = plt.figure()
plt.xlim(0, 10)
plt.ylim(0, 30)
def animate(i):
    lines = plt.plot([x_1[i], x_2[i]], [y_1[i], y_2[i]], 'ok-')
    return lines

ani = animation.FuncAnimation(
    fig, animate, len(t), interval=0.01, blit=True)
plt.show()