from tkinter import END
from typing import List, Dict, Tuple, Union
import numpy as np


THIS FILE WAS DEVIATED TO POINT THE DIFFERENCES BETWEEN CHOOSING
TO SKIP FINDING ANOTHER NODE IF THE START WAS FOUND ON AN EDGE
OF AN EXISTING CIRCLE BUT THEN GAVE UP ON TRYING TO FIND A END

THIS MAY BE WHAT RUINS THE ALGORITHM AND THUS CALLS FOR ANOTHER
VERSION WHERE THIS FILE WILL SKIP THE END




## ===============================================================
#HEAD Constants
## ===============================================================

FILENAME: str = "gen-graph2.txt"
EDGES: str = "edges"
WEIGHT: str = "weight"
NAME: str = "vertex"
MIN_1: int = 0
MIN_2: int = 1

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

nums = np.loadtxt(FILENAME, dtype="i", delimiter=" ")

graphDict: Dict[int, Dict[int, int]] = {i: {j: edge for j, edge in enumerate(vert) if edge > 0} for i, vert in enumerate(nums)}
graphTemp: Dict[int, Dict[str, Union[int, List[int]]]] = {}
graph: List[Dict[str, Union[int, List[int]]]] = []

for key, value in graphDict.items():
  sortedEdges = sorted(value.items(), key=lambda i: i[1])
  edges = [i[0] for i in sortedEdges]
  weight = sum(i[1] for i in sortedEdges)
  vertDict = { WEIGHT: weight, EDGES: edges }
  graphTemp[key] = vertDict

sortedGraphTuple: List[Tuple[int, Dict[str, any]]] = sorted(graphTemp.items(), reverse=True, key=lambda i: i[1][WEIGHT])

for i, tup in enumerate(sortedGraphTuple):
  vertex = tup[0]
  tup[1].update({ NAME: vertex })
  graph.append(tup[1])

#print(graph)

## ===============================================================
#HEAD Algorithm
## ===============================================================

tsp: List[LinkedList] = []
numVert: int = len(graph)

for v in graph:
  if len(tsp) > 0 and len(tsp[0].middle) + 2 > numVert:
    break
  
  alreadyAdded = False

  circle = False

  for ll in tsp:
    if ll.middle.get(v[NAME]):
      circle = True
      break
    if ll.start == v[NAME] or ll.end == v[NAME]:
      circle = ll
      break

  if circle == True:
    continue


  # loop through edges on v to find new start
  # check if already a start or end
  #   if so, combine two groups
  # loop through edges on v to find new end
  # check if already a start or end
  #   if so, combine two groups
  #! Vertex is not on any edges
  if circle == False:

    node = Node(v[NAME])
    isStart = False
    startEndProcess = False
    circleStart = None
    circleEnd = None

    for edge in v[EDGES]:
      if circleStart == None:
        isMiddle = False
        for ll in tsp:
          if inMiddle(ll, edge):
            isMiddle = True
            break
          elif edge == ll.start.data:
            ll.start.start = node
            node.end = ll.start

            ll.middle.update({ ll.start.data: ll.start })

            ll.start = node
            circleStart = node
            break

          elif edge == ll.end.data:
            ll.end.end = node
            node.start = ll.end

            ll.middle.update({ ll.end.data: ll.end })
            
            ll.end = node
            circleStart = node
            break

        if isMiddle == False:
          circleStart = Node(edge)
          node.start = circleStart
          circleStart.end = node
        

      else:
        isMiddle = False
        for ll in tsp:
          if inMiddle(ll, edge):
            isMiddle = True
            break
          if edge == ll.start.data:
            ll.start.start = node
            node.end = ll.start

            ll.start = node
            newStart = True

          elif edge == ll.end.data:
            ll.end.end = node
            node.start = ll.end
            
            ll.end = node
            newStart = True

        if newStart == True:
          continue


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


#DESC Vertex is on a start
    if v[NAME] == ll.start.data:
      newStart = 0
      inTsp = False

      #X If node is in middle or will close circuit keep iterating
      for edge in v[EDGES]:
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
    elif v[NAME] == ll.end.data:
## ===============================================================
      
      newEnd = 0
      inTsp = False

      #X If node is in middle or will close circuit keep iterating
      for edge in v[EDGES]:
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
    elif ll.middle.get(v[NAME]):
## ===============================================================
        
      alreadyAdded = True
      break



printLL(tsp[0])
