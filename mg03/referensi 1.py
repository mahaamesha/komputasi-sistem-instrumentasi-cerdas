import math
import matplotlib.pyplot as plt
import matplotlib.animation as ani

x1 = [5]
y1 = [10]
vx1 = [0]
vy1 = [0]
ax1 = [0]
ay1 = [0]
x2 = [7]
y2 = [8]
vx2 = [0]
vy2 = [0]
ax2 = [0]
ay2 = [0]
l = [math.sqrt((x2[0]-x1[0])*(x2[0]-x1[0])+(y2[0]-y1[0])*(y2[0]-y1[0]))]
F = [0]
Fx1 = [F[0]* (x2[0]-x1[0]) / l[0]]
Fy1 = [F[0]*(y2[0]-y1[0])/l[0]]
Fx2 = [F[0]*(x1[0]-x2[0])/l[0]]
Fy2 = [F[0]*(y1[0]-y2[0])/l[0]]
m1 = 2
m2 = 2
t = [0]
g = 9.8
k = 500
v1 = [math.sqrt(vx1[0]*vx1[0]+vy1[0]*vy1[0])]
v2 = [math.sqrt(vx2[0]*vx2[0]+vy2[0]*vy2[0])]
Ek1 = [m1*v1[0]*v1[0]/2]
Ep1 = [m1*g*y1[0]]
Em1 = [Ek1[0]+Ep1[0]]
Ek2 = [m2*v2[0]*v2[0]/2]
Ep2 = [m2*g*y2[0]]
Em2 = [Ek2[0]+Ep2[0]]
W = [k*(l[-1]-l[0])*(l[-1]-l[0])/2]
E = [Em1[0]+Em2[0]+W[0]]
dt = 0.001

stop_cond = y1[-1]>0.001 or abs(vy1[-1])>0.01 or y2[-1]>0.001 or abs(vy2[-1])>0.01
# stop_cond = y1[-1]<0.001 and abs(vy1[-1])<0.01 and y2[-1]<0.001 and abs(vy2[-1])<0.01
while stop_cond:
    vx1.append (vx1[-1]+ax1[-1]*dt)
    vx2.append (vx2[-1]+ax2[-1]*dt)
    if y1[-1]<0.001 and vy1[-1]<0:
        vy1.append (-0.8*vy1[-1]+ay1[-1]*dt)
    else:
        vy1.append (vy1[-1]-(g-ay1[-1])*dt)
    if y2[-1]<0.001 and vy2[-1]<0:
        vy2.append (-0.8*vy2[-1]+ay2[-1]*dt)
    else:
        vy2.append (vy2[-1]-(g-ay2[-1])*dt)
    x1.append (x1[-1]+vx1[-1]*dt)
    x2.append (x2[-1]+vx2[-1]*dt)
    y1.append (y1[-1]+vy1[-1]*dt)
    y2.append (y2[-1]+vy2[-1]*dt)
    l.append (math.sqrt((x2[-1]-x1[-1])*(x2[-1]-x1[-1])+(y2[-1]-y1[-1])*(y2[-1]-y1[-1])))
    F.append (k*(l[-1]-l[0]))
    Fx1.append (F[-1]*(x2[-1]-x1[-1])/l[-1])
    Fy1.append (F[-1]*(y2[-1]-y1[-1])/l[-1])
    Fx2.append (F[-1]*(x1[-1]-x2[-1])/l[-1])
    Fy2.append (F[-1]*(y1[-1]-y2[-1])/l[-1])
    ax1.append (Fx1[-1]/m1)
    ay1.append (Fy1[-1]/m1)
    ax2.append (Fx2[-1]/m2)
    ay2.append (Fy2[-1]/m2)
    v1.append (math.sqrt(vx1[-1]*vx1[-1]+vy1[-1]*vy1[-1]))
    v2.append (math.sqrt(vx2[-1]*vx2[-1]+vy2[-1]*vy2[-1]))
    Ek1.append (m1*v1[-1]*v1[-1]/2)
    Ep1.append (m1*g*y1[-1])
    Em1.append (Ek1[-1]+Ep1[-1])
    Ek2.append (m2*v2[-1]*v2[-1]/2)
    Ep2.append (m2*g*y2[-1])
    Em2.append (Ek2[-1]+Ep2[-1])
    W.append (k*(l[-1]-l[0])*(l[-1]-l[0])/2)
    E.append (Em1[-1]+Em2[-1]+W[-1])
    t.append (t[-1]+dt)

print ("Benda berhenti saat t =", round(t[-1], 3), "s")

plt.plot (t, Ep1)
plt.plot (t, Ek1)
plt.plot (t, Em1)
plt.legend (["Energi Potensial", "Energi Kinetik", "Energi Mekanik"])
plt.title ("Kurva Energi terhadap Waktu Benda 1")
plt.xlabel ("Waktu (s)")
plt.ylabel ("Energi (J)")
plt.grid (axis = "y")
plt.show ()

plt.plot (t, Ep2)
plt.plot (t, Ek2)
plt.plot (t, Em2)
plt.legend (["Energi Potensial", "Energi Kinetik", "Energi Mekanik"])
plt.title ("Kurva Energi terhadap Waktu Benda 2")
plt.xlabel ("Waktu (s)")
plt.ylabel ("Energi (J)")
plt.grid (axis = "y")
plt.show ()

plt.plot (t, Em1)
plt.plot (t, Em2)
plt.plot (t, W)
plt.plot (t, E)
plt.legend (["Energi Mekanik Benda 1", "Energi Mekanik Benda 2", "Energi Pegas", "Energi Total"])
plt.title ("Kurva Energi terhadap Waktu")
plt.xlabel ("Waktu (s)")
plt.ylabel ("Energi (J)")
plt.grid (axis = "y")
plt.show ()

def move(i):
    a = plt.plot ([x1[i], x2[i]], [y1[i], y2[i]], 'ob-')
    return a

fig = plt.figure()
plt.ylim (-0.2, 15)
plt.xlim (0, 12)
anim = ani.FuncAnimation (fig, move, len(t), interval = 1, repeat = False, blit = True, cache_frame_data = False)
plt.show()
