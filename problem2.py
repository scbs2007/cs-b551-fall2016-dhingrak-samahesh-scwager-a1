import numpy as np
import heapq
from heapq import heapify, heappush, heappop

initial_state = [['11', '14', '01', '0'], ['02', '13', '09', '06'], ['04', '05', '03', '07'], ['10', '15', '12', '08']]

# check parity for the initial state
N = 16
fringe = []
spare_fringe = []
b = []
x = 0
y = 0
a = np.array(initial_state)
solvable_list = []
stats_solve = []


def check_parity(initial_state):
    count = 0
    row_number = 0
    for i in range(0, N):
        for j in range(i + 1, N):
            if int(initial_state[i]) > int(initial_state[j]) and initial_state[j] != '0':
                count += 1
            elif initial_state[j] == '0':
                row_number = j // 4
    solvable_list.append(count)
    solvable_list.append(row_number)
    return(solvable_list)


def successor(initial_state):
    return (create_states(a))


def create_states(a):
    for i in range(0, 4):
        for j in range(0, 4):
            if a[i][j] == '0':
                # to make a copy that doesn't change the original matrix
                b = np.copy(a)
                # store the value of 0 position
                x = i
                y = j
                b[x][y] = b[x][y - 1]
                b[x][y - 1] = '0'
                fringe.append(b)
                b = np.copy(a)
                b[x][y] = b[x - 1][y]
                b[x - 1][y] = '0'
                fringe.append(b)
                b = np.copy(a)
                b[x][y] = b[x + 1][y]
                b[x + 1][y] = '0'
                fringe.append(b)
                b = np.copy(a)
                b[x][y] = b[x][y + 1]
                b[x][y + 1] = '0'
                fringe.append(b)
    return (fringe)


def solve(initial_state):
    fringe = [initial_state]
    pf = a.flatten()
    stats_solve = check_parity(pf)
    if (stats_solve[1] == 0 or stats_solve[1] == 2) and (stats_solve[0])%2 == 1:
        while len(fringe) > 0:
            for s in create_states(a):
                print ('states:' ,fringe)
                fringe.append(s)
                return False


def heuristic_misplacetiles(initial_state):
    while len(fringe) > 0:
        temp = fringe.pop()
        mis_pl = 0
        for i in range(0, 4):
            for j in range(0, 4):
                if goal_state[i][j] != temp[i][j]:
                    mis_pl = mis_pl + 1
        heappush(h, (mis_pl, temp))
        return (heappop(h))

solution = solve(initial_state)