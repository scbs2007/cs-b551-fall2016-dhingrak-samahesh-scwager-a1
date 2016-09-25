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
    
def print_board(a):
    printable = ""
    for i, m in enumerate(a[1], 1):  
        printable += str(m) + ['\t', '\n'][i % 4 == 0]
    print printable
    
def check_parity(board):
    print "checking parity"
    count = 0
    for i in range(N):
        count += i//4 + 1 if board[i] == 0 else len( [ x for x in board[i:N] if x > 0 and x < board[i] ] )
        print "curr tile", board[i], "count", count
    print "is the board even? ", count % 2 == 0
    return count % 2 == 0

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
        
def mh(state, a): #manhattan heuristic
    for i in range(0, 4):
        for j in range(0, 4):
            value = state[i][j]
            goal_index = goal_dict[value]
            a = a + abs(i // 4 - goal_index[0]) + abs(j - goal_index[1])
    return a 
    
    
def successor_mh(curr, goal):
    successor = []
    pos = curr[1]
    depth = curr[0]
    #case 1: left moves are allowed
    if pos in set( range(N) ) - set( [4, 8] ): 
        if pos in [0, 12]:
            successor.append( (depth, pos+3) )
        else: 
            successor.append( (depth, pos-1) )
    #case 2: right moves are allowed
    if pos in set( range(N) ) - set( [7, 11] ): 
        if pos in [3, 15]:
            successor.append( (depth, pos-3) )
        else:
            successor.append( (depth, pos+1) )
    #case 3: upward moves are allowed
    if pos in set( range(N) ) - set( [1, 2] ): 
        if pos in [0, 3]:
            successor.append( (depth, pos+12) )
        else: 
            successor.append( (depth, pos-4) )
    #case 4: downward moves are allowed
    if pos in set( range(N) ) - set( [13, 14] ): 
        if pos in [12, 15]:
            successor.append( (depth, pos-12) )
        else:
            successor.append( (depth, pos+4) )
    print "pos", pos, "goal", goal, "successor", successor
    return successor

def find_shortest_path_mh(pos, goal):
    print "pos", pos
    visited = set(pos)
    fringe = [ (0, pos) ]
    while True:
        curr = heappop(fringe)
        visited |= curr[1] #add position to explored
        if curr[1] == goal:
            return curr[0] #the minimum distance
        for s in successor_mh(curr):
            if s[1] not in visited and s not in fringe:
                heappush(fringe, s) 
    print "there was a bug"
    
def mh(board): #manhattan heuristic taking into account option of jumping between corners
    print "board", board
    total_moves = 0
    for i in range(N):
        if board[i] == 0: #empty tile
            continue
        total_moves += find_shortest_path_mh(i, board[i] - 1) #goal index is 1 less than the number on the tile
    return total_moves

# function for generating various states of the puzzle
def successor(a):
    successors = []
    pos = a[1].index(0) #position of zero tile
    g = a[2] + 1 #add 1 to current depth
    #case 1: left moves are allowed
    if pos in set( range(N) ) - set( [4, 8] ): 
        b = copy.deepcopy(a)[1]
        if pos in [0, 12]:
            b[pos], b[pos+3] = b[pos+3], b[pos]
        else: 
            b[pos], b[pos-1] = b[pos-1], b[pos]
        h = mh(b)
        successors.append( (g+h, b, g) )
    #case 2: right moves are allowed
    if pos in set( range(N) ) - set( [7, 11] ): 
        b = copy.deepcopy(a)[1]
        if pos in [3, 15]:
            b[pos], b[pos-3] = b[pos-3], b[pos]
        else:
            b[pos], b[pos+1] = b[pos+1], b[pos]
        h = mh(b)
        successors.append( (g+h, b, g) )
    #case 3: upward moves are allowed
    if pos in set( range(N) ) - set( [1, 2] ): 
        b = copy.deepcopy(a)[1]
        if pos in [0, 3]:
            b[pos], b[pos+12] = b[pos+12], b[pos]
        else: 
            b[pos], b[pos-4] = b[pos-4], b[pos]
        h = mh(b)
        successors.append( (g+h, b, g) )  
    #case 4: downward moves are allowed
    if pos in set( range(N) ) - set( [13, 14] ): 
        b = copy.deepcopy(a)[1]
        if pos in [12, 15]:
            b[pos], b[pos-12] = b[pos-12], b[pos]
        else: 
            b[pos], b[pos+4] = b[pos+4], b[pos]
        h = mh(b)
        successors.append( (g+h, b, g) ) 
    print "successors:"
    for s in successors: print_board(s)
    return successors


def solve(initial_state):
    fringe = [ (0, initial_state, 0) ] #evaluation function (f = g+h); board; depth of state
#    while len(fringe) > 0: #comment this out to actually run the program
    for i in range(3):
        curr = heappop(fringe)
        print "curr", "f = ", curr[0], "depth = ", curr[2]
        print_board(curr)
        #check is this the solution
        for s in successor(curr):
            fringe.append(s)
    return False

if "__main__" == __name__:
    input_board_filename = str(sys.argv[1])
    if(len(sys.argv) < 2):                                                                                
        print("Please enter file name! python solver15.py input_board.txt")                                                          
        sys.exit(0)
    initial_state = read_board(input_board_filename)
    if not check_parity(initial_state):
        print "This board is not solvable because of its parity."
        quit()
    solve(initial_state)
