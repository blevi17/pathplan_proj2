# Project 2 functions by Levi Butler
import numpy as np
from queue import PriorityQueue

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
    elif 455 <= x <= 510.59 and 125 <= y <= 230:
            if x == 510.59 and y == 125:
                work_res = 0
            elif x == 510:
                work_res = 1
            elif ((125 - y)/(510.59 - x)) >= -2:
                work_res = 0
    # Bottom Part of the Triangle
    elif 455 <= x <= 510.59 and 20 <= y < 125:
        if x == 510 and y == 125:
            work_res = 0
        elif x == 510:
            work_res = 1
        elif 0 <= ((125 - y) / (510.59 - x)) <= 2:
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


def p2_repeat_cl(qu, loc):
    len = qu.qsize()
    res_cl = 0
    for i1 in range(0, len):
        if qu.queue[i1][4] == loc:
            res_cl = 1

    return res_cl

# only to be used when it is known there is a repeat in the closed list
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
