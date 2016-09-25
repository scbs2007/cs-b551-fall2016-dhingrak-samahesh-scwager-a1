import numpy as np
import heapq
from heapq import heapify, heappush, heappop
import sys
import copy

# initializing the variables
N = 16
fringe = []
b = []
solvable_list = []
stats_solve = []
h = []
dis = 0
ef = []


#initial_state = [[11, 14, 1, 0], [2, 13, 9, 6], [4, 5, 3, 7], [10, 15, 12, 8]]
initial_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 0], [13, 14, 15, 12]]
# creating a copy of the initial state of the puzzle


# state to achieve
goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

# dictionary for reference for calculating the manhattan distance
goal_dict = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3], 5: [1, 0], 6: [1, 1], 7: [1, 2], 8: [1, 3], 9: [2, 0],
             10: [2, 1], 11: [2, 2], 12: [2, 3], 13: [3, 0], 14: [3, 1], 15: [3, 2], 0: [3, 3]}


# function for reading the initial condition of the board from the file
def read_board(filename):
    initial_board = []
    with open(filename, "r") as file:
     for line in file:
            initial_board = initial_board + map(int, line.split())
    file.close()
    print "read initial board", initial_board
    return initial_board


# checking the parity of the initial state using method of inversions
def check_parity(p):
    count = 0
    row_number = 0
    for i in range(0, N):
        for j in range(i + 1, N):
            if int(p[i]) > int(p[j]) and p[j] != 0:
                count += 1
            elif p[j] == 0:
                row_number = j // 4
    solvable_list.append(count)
    solvable_list.append(row_number)
    return (solvable_list)


# function for generating various state of the puzzle
def create_states(a):
    for i in range(0, 4):
        for j in range(0, 4):
            if a[i][j] == 0:
                # to make a copy that doesn't change the original matrix
                b = copy.deepcopy(a)
                # store the value of 0 position
                x = i
                y = j
                # do it for four different state
                # put an if for checking the possiblility of the edge
                b[x][y] = b[x][y - 1]
                b[x][y - 1] = 0
                fringe.append(b)
                b = copy.deepcopy(a)
                b[x][y] = b[x - 1][y]
                b[x - 1][y] = 0
                fringe.append(b)
                b = copy.deepcopy(a)
                if x == 3:
                    x = -1
                    b[x][y] = b[x + 1][y]
                    b[x + 1][y] = 0
                    fringe.append(b)
                else:
                    b[x][y] = b[x + 1][y]
                    b[x + 1][y] = 0
                    fringe.append(b)
                b = copy.deepcopy(a)
                if y == 3:
                    y = -1
                    b[x][y] = b[x][y + 1]
                    b[x][y + 1] = 0
                    fringe.append(b)
                else:
                    b[x][y] = b[x][y + 1]
                    b[x][y + 1] = 0
                    fringe.append(b)
        return [fringe]


# function for solution representation

def solver (a):
    temp = np.array(a)
    pf = temp.flatten()
    fringe = copy.deepcopy(a)
    ef = check_parity(pf)
    if (ef[ 1 ] == 0 or ef[ 1 ] == 2) and ef[ 0 ] % 2 == 1:
        while len(fringe) > 0:
            for s in create_states(fringe.pop()):
                distance = mh(s, dis)
                h = heappush(s, distance)
                if distance == 0:
                    return (s)








            # def heuristic_misplacetiles(initial_state):
            #   while len(fringe) > 0:
            #      temp = fringe.pop()
            #     mis_pl = 0
            #    for i in range(0, 4):
            #       for j in range(0, 4):
            #          if goal_state[i][j] != temp[i][j]:
            #             mis_pl += 1
            # heappush(h, (mis_pl, temp))
            # return [heappop(h)]






#            worked around for initial board read
#           Derived with help of teammate Sanna Wager
if "__main__" == __name__:
    input_board_filename = str(sys.argv[1])
    if not check_parity(initial_state):
        print "This board is not solvable because of its parity."
        quit()
        solver(initial_state)


#def solver(initial_state):
 #   fringe = copy.deepcopy(initial_state)
  #
   # for s in create_states(fringe.pop()):
    #    distance = mh(s)
     #   h = heappush(distance, s)
      #  print ['heap', h]


def mh(state, a):
    for i in range(0, 4):
        for j in range(0, 4):
            value = state[i][j]
            goal_index = goal_dict[value]
            a = a + abs(i // 4 - goal_index[0]) + abs(j - goal_index[1])
    return a


solution = solver(initial_state)

print ('done',  solution)


