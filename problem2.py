import numpy as np
import heapq
from heapq import heapify, heappush, heappop
import sys

initial_state = [['11', '14', '01', '0'], ['02', '13', '09', '06'], ['04', '05', '03', '07'], ['10', '15', '12', '08']]
goal_state = [['1' ,'2' ,'3' ,'4'],['5' ,'6' ,'7' ,'8'],['9' ,'10' ,'11' ,'12'],['13' ,'14' ,'15' ,'0']]

# check parity for the initial state
N = 16
fringe = []
spare_fringe = []
b = []
a = np.array(initial_state)
solvable_list = []
stats_solve = []
h = []


def read_board(filename):
    initial_board = []
    with open(filename, "r") as file:
        for line in file:
            initial_board = initial_board + map(int, line.split())
    file.close()
    print "read initial board", initial_board
    return initial_board

def check_parity(p):
    count = 0
    row_number = 0
    for i in range(0, N):
        for j in range(i + 1, N):
            if int(p[i]) > int(p[j]) and p[j] != '0':
                count += 1
            elif p[j] == '0':
                row_number = j // 4
    solvable_list.append(count)
    solvable_list.append(row_number)
    return (solvable_list)


def successor(a):
    return [create_states(a)]


def create_states(a):
    x = 0
    y = 0
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
    fringe = np.copy(a)
    pf = a.flatten()
    stats_solve = check_parity(pf)
    if (stats_solve[1] == 0 or stats_solve[1] == 2) and (stats_solve[0])%2 == 1:
        while len(fringe) > 0:
            for s in create_states(fringe.pop()):
                print ('states:' ,fringe)
                np.append(s)
                return False


def heuristic_misplacetiles(initial_state):
    while len(fringe) > 0:
        temp = fringe.pop()
        mis_pl = 0
        for i in range(0, 4):
            for j in range(0, 4):
                if goal_state[i][j] != temp[i][j]:
                    mis_pl += 1
        heappush(h, (mis_pl, temp))
        return (heappop(h))

# worked around for initial board read
# Derived with help of teammate Sanna Wager
    if "__main__" == __name__:
        input_board_filename = str(sys.argv[1])
        initial_state = read_board(input_board_filename)
        if not check_parity(initial_state):
            print "This board is not solvable because of its parity."
            quit()
        solve(initial_state)
