# TUGAS MANDIRI 1 - SOAL 2
# Nama: Avima Haamesha
# NIM: 10219084

import matplotlib.pyplot as plt

arr_h = [5]
arr_v = [0]

g = 9.8
e = 0.8     # koef restitusi
koef_a = 0.01   # koef perlambatan saat h = 1/2 ho

dt = 1e-2
arr_t = [0]

epsilon = 1e-3  # nol jika kurang dari epsilon

def func_hi(hi_1, vi, dt):
    hi = hi_1 - vi * dt
    return hi

def func_vi(v1_1, g, dt):
    vi = v1_1 + g * dt
    return vi

while not( (abs(arr_v[-1]) < epsilon) and (arr_h[-1] < epsilon) ):     # belum berhenti
    # ketinggian berkurang
    hi = func_hi(arr_h[-1], arr_v[-1], dt)
    arr_h.append(hi)

    # jika mencapai lantai, ubah arah kecepatan
    if (arr_h[-1] < epsilon):
        vi = -e * arr_v[-1]
    else:   # jika di udara, berlaku GLBB
        # ada faktor perlambatan saat h = 1/2 ho
        if hi > 1/2*arr_h[0]:
            a = -koef_a * arr_v[-1]
        else: a = 0
        vi = func_vi(arr_v[-1], (g+a), dt)
    arr_v.append(vi)

    t = arr_t[-1] + dt
    arr_t.append(t)
    
    # print(vi, hi, t)

print("Waktu hingga bola berhenti: %s sekon" %t)


# plotting data untuk cek validasi hasil
fig, axs = plt.subplots(nrows=2, ncols=1, constrained_layout=True)
fig.suptitle("Plot Soal 1")

# plot ketinggian terhadap waktu
axs[0].set_title("h vs t")
axs[0].plot(arr_t, arr_h)
axs[0].set_ylabel("Ketinggian (m)")

# plot kecepatan terhadap waktu
axs[1].set_title("v vs t")
axs[1].plot(arr_t, arr_v)
axs[1].set_ylabel("Kecepatan (m/s²)")

for ax in axs:
    ax.set_xlabel("Waktu (s)")
    ax.grid(True)

plt.show()