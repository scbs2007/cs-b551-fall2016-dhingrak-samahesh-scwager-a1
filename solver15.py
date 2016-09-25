import numpy as np
import copy
import heapq
from heapq import *
import sys

N = 16
solution = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]

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
    return count % 2 == 0

def successor_mh(curr):
    successor = []
    pos = curr[1]
    depth = curr[0] + 1
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
    return successor

def find_shortest_path_mh(pos, goal):
    visited = set([pos])
    fringe = [ (0, pos) ]
    while True:
        curr = heappop(fringe)
        visited.add( curr[1] ) #add position to explored
        if curr[1] == goal:
            return curr[0] #the minimum distance
        for s in successor_mh(curr):
            if s[1] not in visited and s not in fringe:
                heappush(fringe, s) 
    
def mh(board): #manhattan heuristic taking into account option of jumping between corners
    #print "calculating manhattan distance for board: ", board
    total_moves = 0
    for i in range(N):
        if board[i] == 0: #empty tile
            continue
        total_moves += find_shortest_path_mh(i, board[i] - 1) #goal index is 1 less than the number on the tile
    #print "total manhattan distance", total_moves
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
    return successors


def solve(initial_state):
    fringe = [ (0, initial_state, 0) ] #evaluation function (f = g+h); board; depth of state
    while len(fringe) > 0: #comment this out to actually run the program
        curr = heappop(fringe)
        print "current state:", "f = ", curr[0], "depth = ", curr[2], "board:\n"
        print_board(curr)
        if curr[1] == solution:
            print "solution found. now need to backtrack."
            return True
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
