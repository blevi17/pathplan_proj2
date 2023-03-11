#Project 2 Animation file by Levi Butler
from project2_functions import *
from queue import PriorityQueue
import matplotlib.pyplot as plt
from matplotlib import animation

# Bring in all of the .csv files
# initial node [10, 10]
# goal node [530, 200]
# Bring in the data from the other code
# obstacles
data1 = np.loadtxt("proj2_obs.csv", delimiter=",", dtype=float)
x_obs = data1[:, 0]
y_obs = data1[:, 1]
# buffer
data2 = np.loadtxt("proj2_buff.csv", delimiter=",", dtype=float)
x_buff = data2[:, 0]
y_buff = data2[:, 1]
# all closed list points explored
data3 = np.loadtxt("proj2_q2.csv", delimiter=",", dtype=float)
x_exp1 = data3[:, 0]
y_exp1 = data3[:, 1]
# all open list points explored
data4 = np.loadtxt("proj2_q1.csv", delimiter=",", dtype=float)
x_exp2 = data4[:, 0]
y_exp2 = data4[:, 1]
# optimal path
data5 = np.loadtxt("proj2_pa.csv", delimiter=",", dtype=float)
x_pa = data5[:, 0]
y_pa = data5[:, 1]

#plotting data
fig = plt.figure()
plt.plot(x_obs, y_obs, 'b.', markersize=1)
plt.plot(x_buff, y_buff, 'r.', markersize=1)
plt.xlim((0, 600))
plt.ylim((0, 250))

# recording some useful lengths
len_cl = len(x_exp1)
len_op = len(x_exp2)
len_pa = len(x_pa)
def animate(i_b):
    i_a = 2000 * i_b
    if 0 <= i_a <= len_cl:
        plt.plot(x_exp1[0:i_a], y_exp1[0:i_a], 'g.', markersize=1)
    elif len_cl < i_a <= (len_op + len_cl):
        plt.plot(x_exp1, y_exp1, 'g.', markersize=1)
        i_g = i_a - len_cl
        plt.plot(x_exp2[0:i_g], y_exp2[0:i_g   ], 'g.', markersize=1)
    else:
        plt.plot(x_exp1, y_exp1, 'g.', markersize=1)
        plt.plot(x_exp2, y_exp2, 'g.', markersize=1)
        i_pat = i_a - len_cl - len_op
        plt.plot(x_pa[0:i_pat], y_pa[0:i_pat], 'm.', markersize=5)

anim = animation.FuncAnimation(fig, animate,
                               frames=(len_cl + len_op + len_pa),
                               interval=1)

plt.show()
