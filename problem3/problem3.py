
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


#want to modify this to first sort the name set in terms of numbers of friends
def assign_awkward_seating(pairs, namelist, table_size):
    tables = {0, namelist.pop} #seat first person at a table
    while(seq): #while the set is not empty. this takes care of checking for the solution
        #need to create a successor function 
        person = namelist.pop()
        
        for t, others in tables.items():
            if something:
            #if no others are friends and the table isn't full, add to this table
                break
            else: #add a new table
        
        
      
if "__main__" == __name__:
    friends_file = sys.argv[1]
    table_size = sys.argv[2]
    
    pairs, namelist = read_friends(friends_file)
    #solve the seating assignments!
    assign_awkward_seating(pairs, namelist, table_size)
