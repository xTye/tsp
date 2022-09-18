from typing import List, Dict, Tuple, Union
import numpy as np

## ===============================================================
#HEAD Constants
## ===============================================================

C_FILENAME: str = "gen-graph2.txt"
C_EDGES: str = "edges"
C_WEIGHT: str = "weight"
C_NAME: str = "vertex"
C_MIN_1: int = 0
C_MIN_2: int = 1

## ===============================================================
#HEAD Classes and Definitions
## ===============================================================

class Node:
  def __init__(self, data: int):
    self.data: int = data
    self.start: Node = None
    self.end: Node = None

class LinkedList:
  def __init__(self, start: Node, end: Node):
    self.start: Node = start
    self.end: Node = end
    self.middle: Dict[int, Node] = {}

def inMiddle(ll, edge):
  return ll.middle.get(edge)

def printLL(ll: LinkedList):
  walk: Node = ll.start
  s = ""
  while walk != None:
    s += str(walk.data) + " "
    walk = walk.end
  print(s)

## ===============================================================
#HEAD Construct sorted 'graph' and 'dictionary'
## ===============================================================

nums = np.loadtxt(C_FILENAME, dtype="i", delimiter=" ")

graphDict: Dict[int, Dict[int, int]] = {i: {j: edge for j, edge in enumerate(vert) if edge > 0} for i, vert in enumerate(nums)}
graphTemp: Dict[int, Dict[str, Union[int, List[int]]]] = {}
graph: List[Dict[str, Union[int, List[int]]]] = []

for key, value in graphDict.items():
  sortedEdges = sorted(value.items(), key=lambda i: i[1])
  edges = [i[0] for i in sortedEdges]
  weight = sum(i[1] for i in sortedEdges)
  vertDict = { C_WEIGHT: weight, C_EDGES: edges }
  graphTemp[key] = vertDict

sortedGraphTuple: List[Tuple[int, Dict[str, any]]] = sorted(graphTemp.items(), reverse=True, key=lambda i: i[1][C_WEIGHT])

for i, tup in enumerate(sortedGraphTuple):
  vertex = tup[0]
  tup[1].update({ C_NAME: vertex })
  graph.append(tup[1])

#print(graph)

## ===============================================================
#HEAD Algorithm
## ===============================================================

tsp: List[LinkedList] = []
numVert: int = len(graph)
curVert: int = 0
hPath: bool = False

## ===============================================================
#DESC Iterate through verticies in graph
for v in graph:
## ===============================================================


## ===============================================================
#DESC Shortest path is calculated
  if curVert > numVert:
## ===============================================================

    break

## ===============================================================
#DESC tsp is empty
#TODO Will probably end up deleting start
  if len(tsp) == 0:
## ===============================================================
    
    start = Node(v[C_EDGES][C_MIN_1])
    end = Node(v[C_EDGES][C_MIN_2])
    node = Node(v[C_NAME])

    #X Connect Nodes
    node.start = start
    node.end = end
    start.end = node
    end.start = node

    #X Add nodes to linked list
    ll = LinkedList(start, end)
    ll.middle.update({ node.data: node })

    tsp.append(ll)

    curVert = 3
  
## ===============================================================
#HEAD Crux of the algorithm
#DESC tsp is not empty
  else:
## ===============================================================
  
    alreadyAdded = False

## ===============================================================
#DESC Iterate through tsp to see if vertex is an edge or in middle
    for ll in tsp:
## ===============================================================
  
## ===============================================================
#DESC Vertex is on a start
      if v[C_NAME] == ll.start.data:
## ===============================================================
        
        newStart = 0
        inTsp = False

        #X If node is in middle or will close circuit keep iterating
        for edge in v[C_EDGES]:
          inTsp = False

          for ll2 in tsp:
            if inMiddle(ll2, edge) or (edge == ll.end.data and curVert < numVert):
              inTsp = True
              break

          if inTsp == False:
            newStart = edge
            break

        #X Add the edge to middle
        oldStart = ll.start
        node = Node(newStart)
        node.end = oldStart
        oldStart.start = node
        ll.middle.update({ oldStart.data: oldStart })
        ll.start = node

        #X Hook up new nodes
        alreadyAdded = True
        curVert = curVert + 1
        break

## ===============================================================
#DESC Vertex is on an end
      elif v[C_NAME] == ll.end.data:
## ===============================================================
      
        newEnd = 0
        inTsp = False

        #X If node is in middle or will close circuit keep iterating
        for edge in v[C_EDGES]:
          inTsp = False

          for ll2 in tsp:
            if inMiddle(ll2, edge) or (edge == ll.start.data and curVert < numVert):
              inTsp = True
              break

          if not inTsp:
            newEnd = edge
            break

        #X Add the edge to the middle
        oldEnd = ll.end
        node = Node(newEnd)
        node.start = oldEnd
        oldEnd.end = node
        ll.middle.update({ oldEnd.data: oldEnd })
        ll.end = node

        #X Hook up new nodes
        alreadyAdded = True
        curVert = curVert + 1
        break

## ===============================================================
#DESC Vertex is in the middle
      elif ll.middle.get(v[C_NAME]):
## ===============================================================
        
        alreadyAdded = True
        break

## ===============================================================
#DESC Vertex is not in tsp
    if not alreadyAdded:
## ===============================================================

      # loop through edges on v to find new start
      # check if already a start or end
      #   if so, combine two groups
      # loop through edges on v to find new end
      # check if already a start or end
      #   if so, combine two groups

      newStart = 0
      newEnd = 0
      inTsp = False
      searchStart = True
      cnt = 0

      #X If node is in middle or will close circuit keep iterating
      for edge in v[C_EDGES]:
        for ll in tsp:
          if inMiddle(ll, edge):
            if searchStart:
              newStart = edge
            else:
              newEnd = edge

            break


        if inTsp == False:
          newStart = edge
          curVert = curVert + 1
          break

        if inTsp2 == False:
          newStart = edge
          break

      #X Add the edge to middle
      oldStart = ll.start
      node = Node(newStart)
      node.end = oldStart
      oldStart.start = node
      ll.middle.update({ oldStart.data: oldStart })
      ll.start = node

      #X Hook up new nodes
      alreadyAdded = True
      curVert = curVert + 1
      break

#if hPath:
printLL(tsp[0])
