import copy
import sys
from heapq import *


#returns friend pairs and a list containing all the names
#pairs - assumed to be sparse data -  are stored in an adjacency list.
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


def print_solution( table_config ):
    print "solution: \n"
    for (i, table) in enumerate( table_config[1] ):
        print "table ", i+1, ": ", ", ".join( table )

def count_seated( table_config ):
    return sum( [len(x) for x in table_config[1]] )


def is_solution( table_config, person_count ):
    return count_seated( table_config ) == person_count


def evaluation_function( table_config, person_count ):
    g = len(table_config[1])
    h = person_count - count_seated( table_config )
    return g + h

#def seating_successors( pairs, unseated, table_size, curr ): #version where cost is number of tables
def seating_successors( pairs, person, table_size, curr, person_count ): 
    successors = []
    for (i, table) in enumerate(curr[1]):
        if len( table ) >= table_size or len(table & pairs[person]) > 0:
            continue
        new = copy.deepcopy(curr)
        new[1][i].add( person )
        successors.append( (evaluation_function(new, person_count), new[1]) )
    curr[1].append( {person} )
    successors.append( (evaluation_function(curr, person_count), curr[1]) ) #update the table count #initial cost: number of tables
    return successors

def assign_awkward_seating(pairs, name_list, table_size):
    fringe = []
#    print "pairs", pairs
    person_count = len(name_list)
    heappush( fringe, (1, [ {name_list[0]} ]) ) #priority queue for cost and tables so far
    while True:
        curr = heappop( fringe )
        if is_solution(curr, person_count):
            print_solution( curr )
            return curr
        for s in seating_successors( pairs, name_list[ count_seated(curr) ], table_size, curr, person_count):
            heappush( fringe, s )
    print "The program did not find a solution and probably has a bug."
      

if "__main__" == __name__:
    friends_file = str(sys.argv[1])
    table_size = int(sys.argv[2])    
    pairs, namelist = read_friends(friends_file) #read in the list of names and friendship graph!
    assign_awkward_seating(pairs, namelist, table_size) #solve the assignments!
