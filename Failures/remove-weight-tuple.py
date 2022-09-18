
## Orders the graph object and returns the weight.
## Removed for readability.

import numpy as np

class Node:
  def __init__(self, data):
    self.data = data
    self.start = None
    self.end = None

EDGES = 1
MIN_1_WEIGHT = 0
MIN_2_WEIGHT = 1
VERTEX_NAME = 0

FINAL_ARR = 0

FILENAME = "graph.txt"

def inMiddle(vertex, group, index):
  return group["middle"].get(vertex[EDGES]["edges"][index][VERTEX_NAME])

nums = np.loadtxt(FILENAME, dtype="i", delimiter=" ")

graphDict = {i: {j: edge for j, edge in enumerate(vert) if edge > 0} for i, vert in enumerate(nums)}
graph = {i: {j: edge for j, edge in enumerate(vert) if edge > 0} for i, vert in enumerate(nums)}
  
for key, value in graph.items():
    edges = sorted(value.items(), key=lambda i: i[1])
    weight = sum(i[1] for i in edges)
    vertDict = { "weight": weight, "edges": edges }
    graph[key] = vertDict

graph = sorted(graph.items(), reverse=True, key=lambda i: i[1]["weight"])

tsp = []
numVert = len(graph)
curVert = 0

hPath = False

## vertex     (i, {"weight", "edges"})       {}                            [(i, j)]          (i, j)
## v          [0 or 1]                       ["weight" or "edges"]         [iterable]        [0 or 1]

print(graph)

for v in graph:
  if curVert > numVert:
    break
  if len(tsp) == 0:
    start = v[EDGES]["edges"][MIN_1_WEIGHT][VERTEX_NAME]
    end = v[EDGES]["edges"][MIN_2_WEIGHT][VERTEX_NAME]
    tetrad = Node(v[VERTEX_NAME])
    tsp.append({ "start": start, "middle": {v[VERTEX_NAME]: v[VERTEX_NAME]}, "end": end })

    curVert = curVert + 3
  else:
    alreadyAdded = False

    for group in tsp:
      if v[VERTEX_NAME] == group["start"]:
        oldStart = group["start"]
        group["middle"].update({ oldStart: oldStart })
        newStart = 0
        
        curVert = curVert + 1

        ## If min_2_weight is already in the middle, keep iterating if it is.
        for edges in v[EDGES]["edges"]:
          if inMiddle(v, group, newStart) or (v[EDGES]["edges"][newStart][VERTEX_NAME] == group["end"] and curVert < numVert):
            newStart = newStart + 1
          else:
            break

        group["start"] = v[EDGES]["edges"][newStart][VERTEX_NAME]
        alreadyAdded = True
        break
      elif v[VERTEX_NAME] == group["end"]:
        oldEnd = group["end"]
        group["middle"].update({ oldEnd: oldEnd })
        newEnd = 0

        curVert = curVert + 1

        ## If vertex is already in the middle or if it will close off, keep iterating if it is.
        for edges in v[EDGES]["edges"]:
          if inMiddle(v, group, newEnd) or (v[EDGES]["edges"][newEnd][VERTEX_NAME] == group["start"] and curVert < numVert):
            newEnd = newEnd + 1
          else:
              break
        
        group["start"] = v[EDGES]["edges"][newEnd][VERTEX_NAME]
        alreadyAdded = True
        break

    if not alreadyAdded:
      ## Tomorrow, do test, mow the lawn, and take a break! Maybe discord bot.
      ## loop through edges on v to find new start
      ## check if already a start or end
      ##   if so, combine two groups
      ## loop through edges on v to find new end
      ## check if already a start or end
      ##   if so, combine two groups
      alreadyAdded2 = False
      newStart = 0

      for edges in v[EDGES]["edges"]:
        if inMiddle(v, group, newStart) or (v[EDGES]["edges"][newStart][VERTEX_NAME] == group["end"] and curVert < numVert):
          newStart = newStart + 1
        else:
          break

      for group in tsp:
        if start == group["start"]:
          group["middle"].update({ start: start })
          group["middle"].update({ v[VERTEX_NAME]: v[VERTEX_NAME] })
          group["start"] = end

#if hPath:
print(tsp)
