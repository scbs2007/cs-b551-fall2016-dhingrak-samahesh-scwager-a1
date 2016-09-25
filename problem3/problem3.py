import math
import copy
import sys
from heapq import *
import multiprocessing
import time

'''
To run: python problem3.py <friends_file>

1, 2) Algorithm choice and methods
An iterative deepening implementation of best-first search was used. This is not regular IDFS because g(n) increases only when a table is added,
not when a person is added. We can consider this IDA* with h=0 (consistent but uninformative). Algorithm summary: store values in a stack. Set initial maximum 
depth to the number of tables needed if all tables are seated to their maximum capacity. Then, increase by 1 table at a time.

If, after one minute, Best-first search fails, we propose a reasonable but not optimal solution using A* with a non-admissible heuristic:
g(n) = table count, h(n) = number of unseated people, f(n) = g(n) + h(n). 
A* Algorith summary: in a priority queue, we store unexpanded nodes, checking the one with the lowest evaluation function value for the solution, then expanding it. 
In practice, this solution might give one table more than the optimal solution.

Problem definition:
State space: all configurations of one to the total number of guests seated at any given number of nonempty tables, following the non-friendship and max-size restrictions.
Initial state: seat first person in the list at a single table.
Successor function: choose next person in the list. return all configurations where he/she is added to an existing table or seated alone at a new table
cost function: number of tables

Sources and data generation
We generate test data using random_graph_generator.py, which writes the data into myfriends_tk.txt.
Code modified and largely based on work by Tejas K, found @ https://github.com/tk26/Random-Graph-Builder
timeout function found @ http://stackoverflow.com/questions/492519/timeout-on-a-function-call

3) Difficulties faced: dealing with 3 parameters. It was difficult to assess how the total number of guests versus the maximum number of friends a single person has 
versus the maximum table size affected the running time. Assumptions: a given person will not be friends with most of the list, e.g., the graph is sparse. 
We tried graph size settings such as 500 guests, max number of friends 100.
'''

def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    import signal
    class TimeoutError(Exception):
        pass
    def handler(signum, frame):
        raise TimeoutError()
    # set the timeout handler
    signal.signal(signal.SIGALRM, handler) 
    signal.alarm(timeout_duration)
    try:
        result = func(*args, **kwargs)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)
    return result

def read_friends(filename):
    #returns friend pairs as a dictionary of sets and a list containing all the names
    #pairs - assumed to be sparse data. e.g., if there are 1000 guests, it is unlikely anyone will know everybody! 
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
    #all have been seated
    return count_seated( table_config ) == person_count

def evaluation_function_non_optimal( table_config, person_count, table_size ):
    #g is table count, h is people remaining to be seated. 
    return len(table_config[1]) + person_count - count_seated( table_config )

def evaluation_function_optimal( table_config, person_count, table_size ):
    return len(table_config[1])

def seating_successors( pairs, person, table_size, curr, person_count, is_opt ): 
    successors = [] #list of successor nodes
    for (i, table) in enumerate(curr[1]): #find all possible seatings at currently existing tables
        if len( table ) >= table_size or len(table & pairs[person]) > 0: #if table is full or the person has a friend here
            continue
        new = copy.deepcopy(curr) 
        new[1][i].add( person )
        if is_opt:
            cost = len(new[1])
        else:
            cost = evaluation_function_non_optimal(new, person_count, table_size)
        successors.append( (cost, new[1]) ) #append to successors and evaluate cost and heuristic
    curr[1].append( {person} ) #append to successors seating of person at a new table
    if is_opt:        
        cost = len(curr[1])
    else:
        cost = evaluation_function_non_optimal(curr, person_count, table_size)
    successors.append( (cost, curr[1]) ) #append to successors and evaluate cost and heuristic
    return successors

def assign_awkward_seating_ida_star(pairs, name_list, table_size):
    bound = math.ceil( len(name_list) / float(table_size) ) #maximum number of tables allowed for current iteration
    while bound <= len(name_list):
        fringe = [ (1, [ {name_list[0]} ]) ]
        while fringe:
            curr = fringe.pop()
            for s in seating_successors( pairs, name_list[ count_seated(curr) ], table_size, curr, len(name_list), True ):
                if is_solution(curr, len(name_list) ):
                    print_solution( curr )
                    return curr
                if s[0] <= bound:
                    fringe.append(s)
        bound += 1
    return False        

#find a reasonable solution if the optimal one takes too long to calculate
def assign_awkward_seating_non_optimal(pairs, name_list, table_size):
    fringe = []
    person_count = len(name_list)
    heappush( fringe, (1, [ {name_list[0]} ]) ) #priority queue for cost and tables so far
    while True:
        curr = heappop( fringe ) #choose a low-cost option
        if is_solution(curr, person_count):
            print_solution( curr )
            return curr
        for s in seating_successors( pairs, name_list[ count_seated(curr) ], table_size, curr, person_count, False):
            heappush( fringe, s )
      
if "__main__" == __name__:
    friends_file = str(sys.argv[1])
    table_size = int(sys.argv[2]) #maximum number of people at a given table
    pairs, namelist = read_friends(friends_file) #read in the list of names and friendship graph!
    success = timeout(assign_awkward_seating_ida_star, (pairs, namelist, table_size), timeout_duration=60)
    if not success:
        print "optimal solution search is taking too long. Computing a reasonable, but not necessarily optimal, result."
        assign_awkward_seating_non_optimal(pairs, namelist, table_size) #...or, compute a reasonable result!
