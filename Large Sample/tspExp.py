from sys import maxsize
import sys
from itertools import permutations
import numpy as np
V = 0

FILENAME: str = "gen-graph13.txt"

if len(sys.argv) > 1:
  FILENAME = sys.argv[1]

# implementation of traveling Salesman Problem
def travellingSalesmanProblem(graph, s):
 
    # store all vertex apart from source vertex
    vertex = []
    for i in range(V):
        if i != s:
            vertex.append(i)
 
    # store minimum weight Hamiltonian Cycle
    min_path = maxsize
    next_permutation=permutations(vertex)
    for i in next_permutation:
 
        # store current Path weight(cost)
        current_pathweight = 0
 
        # compute current path weight
        k = s
        for j in i:
            current_pathweight += graph[k][j]
            k = j
        current_pathweight += graph[k][s]
 
        # update minimum
        min_path = min(min_path, current_pathweight)
         
    return min_path
 
 
# Driver Code
if __name__ == "__main__":
 
    nums = np.loadtxt(FILENAME, dtype="i", delimiter=" ")

    # Input Matrix
    graph = [[j for j in vert] for vert in nums]

    V = len(graph)

    s = 0
    done = travellingSalesmanProblem(graph, s)
    print(done)