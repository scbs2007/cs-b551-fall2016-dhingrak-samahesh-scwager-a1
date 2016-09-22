import numpy as np
import copy
import heapq
from heapq import *
import sys

N = 16

def read_board(filename):
    board = []
    with open(filename, "r") as file:
        for line in file:
            board = board + map(int, line.split())
    file.close()
    print "read initial board", board
    return board

def check_parity(board):
    print "checking parity"
    count = 0
    for i in range(N):
        count += i//4 + 1 if board[i] == 0 else len( [ x for x in board[i:N] if x > 0 and x < board[i] ] )
        print "curr tile", board[i], "count", count
    print "is the board even? ", count % 2 == 0
    return count % 2 == 0

def successor(a):
    fringe = []
    i = a.index(0)
    x = i // 4
    y = i % 4
    if a[i] == 0:
        # to make a copy that doesn't change the original matrix
        b = copy.deepcopy(a)[1] #Karun - I had to change this since the array is not np...it does the same thing. the [1] is to extract the board from the list with cost and board
        # store the value of 0 position
        #all possible cases where left swap is possible
        print "b", b
        if y != 0 or y == 0 and x in [0, 4]:
            if y != 0: 
                print "case y != 0", "i=", i, "i-1=", i-1
                b[i], b[i-1] = b[i-1], b[i]
            else: 
                print "case x in [0,4] and y = 0", "i=", i, "i+3=", i+3 
                b[i], b[i+3] = b[i+3], b[i]
                fringe.append( (0, b) ) #cost is set to 0. need to add +1 and the heuristic
                #need to change the three other swaps so that they work for 1-dimensional array. 
#            b[x][y] = b[x][y - 1]
#            b[x][y - 1] = 0
#            fringe.append( (0, b) )
#            b = np.copy(a)
#            b[x][y] = b[x - 1][y]
#            b[x - 1][y] = 0
#            fringe.append( (0, b) )
#            b = np.copy(a)
#            b[x][y] = b[x + 1][y]
#            b[x + 1][y] = 0
#            fringe.append( (0, b) )
#            b = np.copy(a)
#            b[x][y] = b[x][y + 1]
#            b[x][y + 1] = 0
#            fringe.append( (0, b) )
    return fringe


def solve(initial_state):
    fringe = [ (0, initial_state) ]
#    pf = a.flatten()
#    stats_solve = check_parity(pf)
#    if (stats_solve[1] == 0 or stats_solve[1] == 2) and (stats_solve[0])%2 == 1:
#    while len(fringe) > 0:
    for i in range(5):
        curr = heappop(fringe)
        print "curr", curr
        for s in successor(curr):
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


if "__main__" == __name__:
    input_board_filename = str(sys.argv[1])
    initial_state = read_board(input_board_filename)
    if not check_parity(initial_state):
        print "This board is not solvable because of its parity."
        quit()
    solve(initial_state)


# to use the heap, would need to store the states as a list with the cost and the board. e.g.  for s in successor(a):  heappush( fringe, (15, [ s ]) ) #priority queue for cost and tables so far
