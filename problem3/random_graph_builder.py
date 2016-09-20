# Author: Sanna Wager - code modified and largely based on work by Tejas K 
# https://github.com/tk26/Random-Graph-Builder

# Generates a random graph of friends
# Run from shell: python random_graph_builder.py <NumberOfPeople>
# See output file: myfriends_tk.txt
# More: Lower the range of k to get a thinner web
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
print friends

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
