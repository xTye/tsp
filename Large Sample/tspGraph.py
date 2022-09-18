import random as rand
from typing import List

## ===============
#HEAD CONSTANTS
## ===============

C_VERT: int =           11
C_MAX_WEIGHT: int =     12321
C_FILENAME: str =       "gen-graph13.txt"

C_F = open(C_FILENAME, "wt")

## ===============
#HEAD Make graph
## ===============

graph: List[List[int]] = []
iterator = 0

for i in range(C_VERT):
  vertList: List[int] = []
  for j in range(C_VERT):
      vertList.append(graph[j][i]) if j < iterator else vertList.append(rand.randint(1, C_MAX_WEIGHT)) if i != j else vertList.append(0)
  iterator = iterator + 1
  graph.append(vertList)


for i in range(C_VERT):
  for j in range(C_VERT):
    if j == C_VERT - 1:
      C_F.write(str(graph[i][j]))
    elif i != j:
      C_F.write(str(graph[i][j]) + " ")
    else:
      C_F.write("0 ")
    if j+1 == C_VERT: C_F.write("\n")

C_F.close()