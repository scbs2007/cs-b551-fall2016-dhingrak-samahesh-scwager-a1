import sys
from heapq import *

#returns friend pairs and a list containing all the names
#pairs - assumed to be sparce data -  are stored in an adjacency list.
def read_friends(filename):
    name_set = set()
    with open(filename, "r") as file:
       for line in file:
           name_set |= set(line.split())
    file.close()
    pairs = {key: set() for key in name_set}
    with open(filename, "r") as file:
       for line in file:
           n = line.split()
           pairs[ n[0] ] |= set(n[1:])
           for i in n[1:]:
               pairs[i].add(n[0])
    return pairs, list(name_set)

def seating_successors( pairs, unseated, table_size, curr ):
    successors = []
    person = unseated.pop()
    found_spot = False
    for table in curr[1]:
        print "table", table
        if found_spot is True:
            break
        if len( table ) >= table_size:
            continue
        table.append( person )
        found_spot = True 
    if found_spot is False:
        curr[1].append( [person] )
    print "curr", curr
    successors.append(curr)
    return successors
    
    

def assign_awkward_seating(pairs, name_list, table_size):
    fringe = []
    heappush( fringe, (1, [ [name_list.pop()] ]) ) #priority queue for cost and tables so far
    while (name_list):
        print "fringe", fringe
        curr = heappop( fringe )
        if not name_list:
            print "solution", curr
            return curr
        for s in seating_successors( pairs, name_list, table_size, curr):
            heappush( fringe, s )
    print "The program did not find a solution and probably has a bug."
        
        
      
if "__main__" == __name__:
    friends_file = sys.argv[1]
    table_size = sys.argv[2]
    
    pairs, namelist = read_friends(friends_file)
    #solve the seating assignments!
    assign_awkward_seating(pairs, namelist, table_size)
