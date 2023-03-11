# Path Planning Project by Levi Butler
from queue import PriorityQueue
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

####################### project2_functions.py #################################################
# This python file checks for collisions taking the 5 mm buffer into account
def p2_coll(loc):
    work_res = 1
    x = loc[0]
    y = loc[1]
    sh = 1 / np.sqrt(3)
    # outer wall
    if x < 5 or y < 5 or x > 595 or y > 245:
        work_res = 0
    # Bottom Rectangle
    elif 95 <= x <= 155 and y <=105:
        work_res = 0
    # Top Rectangle
    elif 95 <= x <= 155 and y >= 145:
        work_res = 0
    # Top Part of the Triangle
    elif 455 <= x <= 515.59 and 125 <= y <= 230:
            if x == 515.59 and y == 125:
                work_res = 0
            elif x == 515.59:
                work_res = 1
            elif ((125 - y)/(515.59 - x)) >= -2:
                work_res = 0
    # Bottom Part of the Triangle
    elif 455 <= x <= 515.59 and 20 <= y < 125:
        if x == 515.59 and y == 125:
            work_res = 0
        elif x == 515.59:
            work_res = 1
        elif 0 <= ((125 - y) / (515.59 - x)) <= 2:
            work_res = 0
    # Hexagon Rectangle
    elif 230.05 <= x <= 369.95 and 84.61 <= y <= 165.39:
        work_res = 0
    # Hexagon Top Left Triangle
    elif 230.05 <= x <= 300 and 165.39 < y <= 205.77:
        if x == 230.05 and y == 165.39:
            work_res = 0
        elif x == 230.05:
            work_res = 1
        elif 0 <= ((165.39 - y)/(230.05 - x)) <= sh:
            work_res = 0
    # Hexagon Top Right Triangle
    elif 300 < x <= 369.95 and 165.39 < y <= 205.77:
        if x == 369.95 and y == 165.39:
            work_res = 0
        elif x == 369.95:
            work_res = 1
        elif -sh <= ((165.39 - y)/(369.95 - x)) <= 0:
            work_res = 0
    # Hexagon Bottom Left Triangle
    elif 230.05 <= x <= 300 and 44.22 <= y < 84.61:
        if x == 230.05:
            work_res = 1
        elif -sh <= ((84.61 - y) / (230.05 - x)) <= 0:
            work_res = 0
    # Hexagon Bottom Right Triangle
    elif 300 < x <= 369.95 and 44.22 <= y < 84.61:
        if x == 369.95:
            work_res = 1
        elif 0 <= ((84.61 - y) / (369.95 - x)) <= sh:
            work_res = 0

    return work_res


# This function checks for a repeat position (x,y) in a priority queue
def p2_repeat_cl(qu, loc):
    len = qu.qsize()
    res_cl = 0
    for i1 in range(0, len):
        if qu.queue[i1][4] == loc:
            res_cl = 1

    return res_cl

# only to be used when it is known there is a repeat in the closed list
# this function pulls the current cost of a position
def p2_repeat_op(qu1, loc):
    len = qu1.qsize()
    for i1 in range(0, len):
        if qu1.queue[i1][4] == loc:
            m_co = qu1.queue[i1][0]

    return m_co

# check the last move to ensure they do not go back and forth
def last_move(cm, lm):
    res_lm = 0
    if cm == 0 and lm == 1:
        res_lm = 1
    elif cm == 1 and lm == 0:
        res_lm = 1
    elif cm == 2 and lm == 3:
        res_lm = 1
    elif cm == 3 and lm == 2:
        res_lm = 1
    elif cm == 4 and lm == 7:
        res_lm = 1
    elif cm == 5 and lm == 6:
        res_lm = 1
    elif cm == 6 and lm == 5:
        res_lm = 1
    elif cm == 7 and lm == 4:
        res_lm = 1

    return res_lm


# This reverses a list
def reverse_list(listio):
    new_list = []
    for i_l in range(1, len(listio) + 1):
        new_list.append(listio[-1*i_l])
    return new_list

# This searches through a queue, finding the parents of indexes until it reaches the initial node
def trace_back(q_cl, par, cur_ind):
    path = [cur_ind, par]
    while par != 0:
        len = q_cl.qsize()
        for it in range(0, len):
            if q_cl.queue[it][1] == par:
                path.append(q_cl.queue[it][2])
                par = q_cl.queue[it][2]
    trace_res = reverse_list(path)

    return trace_res

# This checks if a position (x,y) is in the obstacle space
# This code allows the obstackes abd buffer to be seperated into different colors on the graph
def p2_obs(loc):
    work_res = 1
    x = loc[0]
    y = loc[1]
    sh = 1 / np.sqrt(3)
    # Bottom Rectangle
    if 100 <= x <= 150 and y <=100:
        work_res = 0
    # Top Rectangle
    elif 100 <= x <= 150 and y >= 150:
        work_res = 0
    # Top Part of the Triangle
    elif 460 <= x <= 510 and 125 <= y <= 225:
            if x == 510 and y == 125:
                work_res = 0
            elif x == 510:
                work_res = 1
            elif ((125 - y)/(510 - x)) >= -2:
                work_res = 0
    # Bottom Part of the Triangle
    elif 460 <= x <= 510 and 25 <= y < 125:
        if x == 510 and y == 125:
            work_res = 0
        elif x == 510:
            work_res = 1
        elif 0 <= ((125 - y) / (510 - x)) <= 2:
            work_res = 0
    # Hexagon Rectangle
    elif 235.05 <= x <= 364.95 and 87.5 <= y <= 162.5:
        work_res = 0
    # Hexagon Top Left Triangle
    elif 235.05 <= x <= 300 and 162.5 < y <= 200:
        if x == 235.05 and y == 162.5:
            work_res = 0
        elif x == 235.05:
            work_res = 1
        elif 0 <= ((162.5 - y)/(235.05 - x)) <= sh:
            work_res = 0
    # Hexagon Top Right Triangle
    elif 300 < x <= 364.95 and 162.5 < y <= 200:
        if x == 364.95 and y == 162.5:
            work_res = 0
        elif x == 364.95:
            work_res = 1
        elif -sh <= ((162.5 - y)/(364.95 - x)) <= 0:
            work_res = 0
    # Hexagon Bottom Left Triangle
    elif 235.05 <= x <= 300 and 50 <= y < 87.5:
        if x == 230.05:
            work_res = 1
        elif -sh <= ((87.5 - y) / (235.05 - x)) <= 0:
            work_res = 0
    # Hexagon Bottom Right Triangle
    elif 300 < x <= 364.95 and 50 <= y < 87.5:
        if x == 364.95:
            work_res = 1
        elif 0 <= ((87.5 - y) / (364.95 - x)) <= sh:
            work_res = 0

    return work_res


########################################## project2_p1.py #######################################################
# Action Set
act = [[1, 0, 1], [-1, 0, 1], [0, 1, 1], [0, -1, 1], [1, 1, 1.4], [-1, 1, 1.4], [1, -1, 1.4], [-1, -1, 1.4]]

# Initial node and Goal node
x_i = input("Enter x coordinate of initial position:")
y_i = input("Enter y coordinate of initial position:")
x_g = input("Enter x coordinate of goal position:")
y_g = input("Enter y coordinate of goal position:")
anim_speed = input("Enter your animation speed:")
node_i = [int(x_i), int(y_i)]
node_g = [int(x_g), int(y_g)]

# Initialize priority q
q1 = PriorityQueue()
q2 = PriorityQueue()
q3 = PriorityQueue()  # this is just for the while loop
uuu = q3.empty()

# The elements in each list is cost to come, index, parent node, last move, and position
el1 = [0, 1, 0, 12, node_i]
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
            # Check the last move
            check_lm = last_move(i1, cur_lm)
            if check_lm == 0:      # Check the last move, hope to reduce speed
                # Check if the new location is in the closed list or obstacle space
                check_cl = p2_repeat_cl(q2, new_l)
                check_ob = p2_coll(new_l)
                if check_cl == 0 and check_ob == 1:
                    check_ol = p2_repeat_cl(q1, new_l)
                    if check_ol == 0:
                        id = id + 1
                        new_node = [cur_co + lxu, id, cur_i, i1, new_l]
                        q1.put(new_node)
                elif check_cl == 1 and check_ob == 1:
                    m_co = p2_repeat_op(q2, new_l)
                    lenj = q2.qsize()
                    if m_co > (cur_co + lxu):
                        for j1 in range(0, lenj):
                            if q2.queue[j1][4] == new_l:
                                m_i = q2.queue[j1][1]
                                q2.queue[j1] = [cur_co + lxu, m_i, cur_i , i1, new_l]

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

####################################### proj2_animation.py ##################################################
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
# Animation function that starts at the closed loop, moving to the open loop, and then plotting the optimal path
def animate(i_b):
    spe = int(anim_speed)
    i_a = spe * i_b
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

# Plotting the animation
anim = animation.FuncAnimation(fig, animate,
                               frames=(len_cl + len_op + len_pa),
                               interval=1)

plt.show()
