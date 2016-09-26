'''
code modified and largely based on work by Tejas K 
https://github.com/tk26/Random-Graph-Builder

to run: python random_graph_builder <int: number of people> <int: maximum number of friends per person>

Generates a random graph of friends
See output file: myfriends_tk.txt
'''

import random
import numpy as np
import sys
pool = int(sys.argv[1])
max_circle = int(sys.argv[2])
target = []
friends = []
output = ""

friends = [ set() for x in np.random.choice(pool, pool/5, replace=False) ]

for i in range(0, len(friends)):
    circle = set( np.random.choice(pool, np.random.choice(range(1,max_circle+1))) )
    friends[i] |= circle

for i in range(0, len(friends)):
    circle = list(friends[i])
    output += str(circle[0])
    for j in circle[1:]:
        output +=  " "
        output += str(j)
    output += "\n"

print output

text_file = open("myfriends_tk.txt", "w")
text_file.write(output)
text_file.close()
