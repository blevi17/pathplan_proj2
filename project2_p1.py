# Project 2 of Path Planning by Levi Butler
from project2_functions import *
from queue import PriorityQueue
import matplotlib.pyplot as plt

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
node_i = [10, 10]
node_g = [180, 50]

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
    res_g = 1
elif check_i == 0:
    print("The initial node is in the obstacle space")
    res_g = 1
elif check_g == 0:
    print("The goal node is in the obstacle space")
    res_g = 1

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
        print("success")
        res_g = 1

    # perform all possible movements
    else:
        for i1 in range(0, 8):
            mov = act[i1]
            lxu = mov[2]
            new_l = [cur_l[0] + mov[0], cur_l[1] + mov[1]]
            # Check if the new location is in the closed list or obstacle space
            check_cl = p2_repeat_cl(q2, new_l)
            check_ob = p2_coll(new_l)
            check_lm = last_move(i1, cur_lm)
            if check_lm == 0:
                if check_cl == 0 and check_ob == 1 and check_lm == 0:
                    check_ol = p2_repeat_cl(q1, new_l)
                    if check_ol == 0:
                        id = id + 1
                        new_node = [cur_co + lxu, id, cur_i, i1, new_l, 0]
                        q1.put(new_node)
                elif check_cl == 1:
                    m_co = p2_repeat_op(q2, new_l)
                    lenj = q2.qsize()
                    if m_co > (cur_co + lxu):
                        for j1 in range(0, lenj):
                            if q2.queue[j1][4] == new_l:
                                m_i = q2.queue[j1][1]
                                q2.queue[j1] = [cur_co + lxu, m_i, cur_i, i1, new_l, 0]
