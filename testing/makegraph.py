import random as rand
from typing import List

## ===============
#HEAD CONSTANTS
## ===============

C_VERT: int =           5
C_MAX_WEIGHT: int =     10
C_FILENAME: str =       "gen-graphTEST10.txt" 
C_START: int =          ord('A')
C_HAND: bool =          False

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

## ===============
#HEAD Write to file
## ===============

## ===============
#DESC FORM GRAPH FOR HAND CALC
if C_HAND:
## ===============

  vertName = C_START

  C_F.write("\t\t")

  for i in range(C_VERT):
    C_F.write(chr(vertName) + "\t\t")
    if i+1 == C_VERT: C_F.write("SUM\t")
    vertName = vertName + 1

  C_F.write("\n")

  vertName = C_START

  for i in range(C_VERT):
    C_F.write(chr(vertName) + "\t\t")
    vertName = vertName + 1
    for j in range(C_VERT):
        C_F.write(str(graph[i][j]) + "\t\t") if i != j else C_F.write("0\t\t")
        if j+1 == C_VERT: C_F.write(str(sum(graph[i])) +"\n")

## ===============
#DESC FORM GRAPH FOR COMP CALC
else:
## ===============

  for i in range(C_VERT):
    for j in range(C_VERT):
      if j == C_VERT - 1:
        C_F.write(str(graph[i][j]))
      elif i != j:
        C_F.write(str(graph[i][j]) + " ")
      else:
        C_F.write("0 ")
      if j+1 == C_VERT: C_F.write("\n")

## ===============
#HEAD Close file
## ===============

C_F.close()