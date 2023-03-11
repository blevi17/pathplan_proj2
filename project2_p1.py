# Project 2 of Path Planning by Levi Butler
from project2_functions import *
from queue import PriorityQueue
import matplotlib.pyplot as plt
import time

start = time.time()
# Action Set
act = [[1, 0, 1], [-1, 0, 1], [0, 1, 1], [0, -1, 1], [1, 1, 1.4], [-1, 1, 1.4], [1, -1, 1.4], [-1, -1, 1.4]]
#r = [1, 0]  # last move 0
#l = [-1, 0]  # last move 1
#u = [0, 1]  # last move 2
#d = [0, -1]  # last move 3
#ur = [1, 1]  # last move 4
#ul = [-1, 1]  # last move 5
#dr = [1, -1]  # last move 6
#dl = [-1, -1]  # last move 7

# Initial node and Goal node
x_i = input("Enter x coordinate of initial position:")
y_i = input("Enter y coordinate of initial position:")
x_g = input("Enter x coordinate of goal position:")
y_g = input("Enter y coordinate of goal position:")
node_i = [int(x_i), int(y_i)]
node_g = [int(x_g), int(y_g)]

# Initialize priority q
q1 = PriorityQueue()
q2 = PriorityQueue()
q3 = PriorityQueue()  # this is just for the while loop
uuu = q3.empty()

# The elements in each list is cost to come, index, parent node, last move, position, and color
el1 = [0, 1, 0, 12, node_i, 1]
q1.put(el1)


# check if the initial node or goal nodes are in obstacle space
check_i = p2_coll(node_i)
check_g = p2_coll(node_g)
if check_i == 0 and check_g == 0:
    print("The initial node and goal nodes are in the obstacle space")
    exit()
elif check_i == 0:
    print("The initial node is in the obstacle space")
    exit()
elif check_g == 0:
    print("The goal node is in the obstacle space")
    exit()

# Spreading out and looking
res_g = 0
id = 0 # index
while q1.empty() != uuu and res_g == 0:
    # pull out a node and add it to the closed list
    x = q1.get()
    q2.put(x)
    # pull out useful elements
    cur_co = x[0]
    cur_i = x[1]
    cur_p = x[2]
    cur_lm = x[3]
    cur_l = x[4]
    # check if we have reached the goal
    if cur_l == node_g:
        # run the backtrack function
        node_path = trace_back(q2, cur_p, cur_i)
        print("success")
        res_g = 1

    # perform all possible movements
    else:
        for i1 in range(0, 8):
            mov = act[i1]
            lxu = mov[2]
            new_l = [cur_l[0] + mov[0], cur_l[1] + mov[1]]
            # Check the last move so it does not move back and forth
            check_lm = last_move(i1, cur_lm)
            if check_lm == 0:
                # Check if the new location is in the closed list or obstacle space
                check_cl = p2_repeat_cl(q2, new_l)
                check_ob = p2_coll(new_l)
                if check_cl == 0 and check_ob == 1:
                    check_ol = p2_repeat_cl(q1, new_l)
                    if check_ol == 0:
                        id = id + 1
                        new_node = [cur_co + lxu, id, cur_i, i1, new_l, 0]
                        q1.put(new_node)
                elif check_cl == 1 and check_ob == 1:
                    m_co = p2_repeat_op(q2, new_l)
                    lenj = q2.qsize()
                    if m_co > (cur_co + lxu):
                        for j1 in range(0, lenj):
                            if q2.queue[j1][4] == new_l:
                                m_i = q2.queue[j1][1]
                                q2.queue[j1] = [cur_co + lxu, m_i, cur_i, i1, new_l, 0]

# save all explored x and y points
plt1_size = q2.qsize()
x_exp1 = []
y_exp1 = []
for i1_plot in range(0, plt1_size):
    x_exp1.append(q2.queue[i1_plot][4][0])
    y_exp1.append(q2.queue[i1_plot][4][1])

# save the open explored points
plt2_size = q1.qsize()
x_exp2 = []
y_exp2 = []
for i2_plot in range(0, plt2_size):
    x_exp2.append(q1.queue[i2_plot][4][0])
    y_exp2.append(q1.queue[i2_plot][4][1])

# record the path
len_pa = len(node_path)
x_pa = []
y_pa = []
for i_pa in range(0, len_pa):
    ind_pa = node_path[i_pa]
    for j_pa in range(0, plt1_size):
        if q2.queue[j_pa][1] == ind_pa:
            x_pa.append(q2.queue[j_pa][4][0])
            y_pa.append(q2.queue[j_pa][4][1])


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
plt.plot(x_exp1, y_exp1, 'g.', markersize=1)
plt.plot(x_exp2, y_exp2, 'g.', markersize=1)
plt.plot(x_pa, y_pa, 'm.', markersize=5)
plt.xlim((0, 600))
plt.ylim((0, 250))
plt.show()

#create a csv file using numpy, q2 -> x_exp1
ans_p1 = np.zeros((len(x_exp1), 2))
for i1 in range(0, len(x_exp1)):
    ans_p1[i1, 0] = x_exp1[i1]
    ans_p1[i1, 1] = y_exp1[i1]

np.savetxt("proj2_q2.csv",
           ans_p1,
           delimiter =", ",
           fmt ='% s')

#create a csv file using numpy, q1 -> x_exp2
ans_p2 = np.zeros((len(x_exp2), 2))
for i2 in range(0, len(x_exp2)):
    ans_p2[i2, 0] = x_exp2[i2]
    ans_p2[i2, 1] = y_exp2[i2]

np.savetxt("proj2_q1.csv",
           ans_p2,
           delimiter =", ",
           fmt ='% s')

#create a csv file using numpy, path -> x_pa
ans_p3 = np.zeros((len(x_pa), 2))
for i2 in range(0, len(x_pa)):
    ans_p3[i2, 0] = x_pa[i2]
    ans_p3[i2, 1] = y_pa[i2]

np.savetxt("proj2_pa.csv",
           ans_p3,
           delimiter =", ",
           fmt ='% s')

end = time.time()
print(end - start)
