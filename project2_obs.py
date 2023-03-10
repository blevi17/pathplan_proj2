# Project 2 Obstacle Points by Levi Butler
import matplotlib.pyplot as plt
from project2_functions import *
import numpy as np

# Get all of the points for the buffer or an actual obstacle
x_obs = []
y_obs = []
x_buff = []
y_buff = []
for i in range(0, 600):
    for j in range(0, 250):
        loc_p = [i, j]
        if p2_obs(loc_p) == 0:
            x_obs.append(i)
            y_obs.append(j)
        elif p2_coll(loc_p) == 0:
            x_buff.append(i)
            y_buff.append(j)

#plotting data
plt.plot(x_obs, y_obs, 'b.', markersize=1)
plt.plot(x_buff, y_buff, 'r.', markersize=1)
plt.xlim((0, 600))
plt.ylim((0, 250))
plt.show()

#create a csv file using numpy (obstacles)
ans_p1 = np.zeros((len(x_obs), 2))
for i1 in range(0, len(x_obs)):
    ans_p1[i1, 0] = x_obs[i1]
    ans_p1[i1, 1] = y_obs[i1]

np.savetxt("proj2_obs.csv",
           ans_p1,
           delimiter =", ",
           fmt ='% s')

#create a csv file using numpy (buffer)
ans_p2 = np.zeros((len(x_buff), 2))
for i2 in range(0, len(x_buff)):
    ans_p2[i2, 0] = x_buff[i2]
    ans_p2[i2, 1] = y_buff[i2]

np.savetxt("proj2_buff.csv",
           ans_p2,
           delimiter =", ",
           fmt ='% s')
