from typing import List, Dict, Tuple, Union
import numpy as np
import sys

## ===============================================================
#HEAD Constants
## ===============================================================

FILENAME: str = "gen-graph13.txt"
EDGES: str = "edges"
WEIGHT: str = "weight"
NAME: str = "vertex"
MIN_1: int = 0
MIN_2: int = 1
DEBUG: bool = False
DEBUGGRAPH: bool = False

if len(sys.argv) > 1:
  FILENAME = sys.argv[1]

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

def printLLFinal(ll: LinkedList):
  walk: Node = ll.start
  s = ""
  while walk != None:
    s += str(chr((walk.data % 26) + 65)) + " "
    walk = walk.end
  print(s)

def getTot(ll: LinkedList):
  walk: Node = ll.start
  nums = np.loadtxt(FILENAME, dtype="i", delimiter=" ")
  tsp = [[j for j in vert] for i, vert in enumerate(nums)]
  i = 0
  sum = tsp[ll.start.data][ll.end.data]
  while walk.end != None:
    sum += tsp[walk.data][walk.end.data]
    walk = walk.end
    i += 1
  return sum

def printWithEdgeWeight(ll: LinkedList):
  walk: Node = ll.start
  nums = np.loadtxt(FILENAME, dtype="i", delimiter=" ")
  tsp = [[j for j in vert] for i, vert in enumerate(nums)]
  s = str(chr((ll.end.data % 26) + 65)) + "-" + str(tsp[ll.start.data][ll.end.data]) + "-"

  while walk.end != None:
    s += str(chr((walk.data % 26) + 65)) + "-" + str(tsp[walk.data][walk.end.data]) + "-"
    walk = walk.end
  s += str(chr((walk.data % 26) + 65))
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

if DEBUGGRAPH: print(graph)

## ===============================================================
#HEAD Algorithm
## ===============================================================

tsp: List[LinkedList] = []
numVert: int = len(graph)

for v in graph:
  if len(tsp) > 0 and len(tsp[0].middle) + 2 >= numVert:
    break
  
  if DEBUG: print("Vertex:" + str(v[NAME]))

  linkedList = False

  for ll in tsp:
    if ll.middle.get(v[NAME]):
      linkedList = True
      break
    if ll.start.data == v[NAME] or ll.end.data == v[NAME]:
      linkedList = ll
      break

  ## Node is in middle
  if linkedList == True:
    if DEBUG: print("Already in list\n")
    continue

  ## Connect a new node
  elif linkedList == False:
    if DEBUG: print("Not already in a linked list")

    node = Node(v[NAME])
    startNode = None
    endNode = None
    isEnd = False

    for edge in v[EDGES]:
      if DEBUG: print("Edge:" + str(edge))
      if startNode != None and endNode != None:
        break
      if len(tsp) > 0 and len(tsp[0].middle) + 2 >= numVert:
        break
      #! Find startNode
      elif startNode == None:
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
            startNode = node
            linkedList = ll
            break

          elif edge == ll.end.data:
            ll.end.end = node
            node.start = ll.end

            ll.middle.update({ ll.end.data: ll.end })
            
            ll.end = node
            startNode = node
            linkedList = ll
            isEnd = True
            break

        if isMiddle == True:
          continue

        if isMiddle == False and linkedList == False:
          startNode = Node(edge)
          node.start = startNode
          startNode.end = node
      
        if DEBUG: print("Start node:" + str(startNode.data))
        if DEBUG: print("Node:" + str(node.data))
        
      #! Find endNode
      else:
        isMiddle = False
        tempLinkedList = None
        for ll in tsp:
          if inMiddle(ll, edge):
            isMiddle = True
            break
          elif edge == ll.start.data or edge == ll.end.data:
            # Check if close off current loop when at end
            if startNode == node and ll == linkedList and len(ll.middle) + 2 < len(graph):
              isMiddle = True
              break
            tempLinkedList = ll
            break

        if isMiddle == True:
          continue

        # This is to make sure that the first iteration
        # has already been added to an existing linked list
        # also known as linkedList != null
        if startNode == node:
          # Two linked lists don't need to be connected
          #NOTE We are only dealing with one linked list
          if tempLinkedList == None:
            endNode = Node(edge)
            if isEnd == False:
              node.start = endNode
              endNode.end = node
              linkedList.middle.update({ node.data: node })
              linkedList.start = endNode
              break
            else:
              node.end = endNode
              endNode.start = node
              linkedList.middle.update({ node.data: node })
              linkedList.end = endNode
              break
          # We are dealing with two, possibly large linked lists
          # We must merge them
          else:
            # Edge is on the start of the newly created linked list
            if edge == tempLinkedList.start.data:
              # Node is on start of linkedList (Requires rerouting)
              if isEnd == False:
                linkedList.start.start = tempLinkedList.start
                linkedList.middle.update({ linkedList.start.data: linkedList.start })

                tempPrevNode = linkedList.start
                tempNode = tempLinkedList.start
                tempNextNode = tempLinkedList.start.end

                while tempNextNode != None:
                  linkedList.middle.update({ tempNode.data: tempNode })
                  tempNode.start = tempNextNode
                  tempNode.end = tempPrevNode
                  
                  tempPrevNode = tempNode
                  tempNode = tempNextNode
                  tempNextNode = tempNextNode.end

                tempNode.end = tempPrevNode
                tempNode.start = None
                linkedList.start = tempNode

                tsp.remove(tempLinkedList)
                break

              # Node is on end of linkedList (No rerouting)
              else:
                tempNode = tempLinkedList.start
                tempNode.start = linkedList.end
                linkedList.end.end = tempLinkedList.start
                linkedList.middle.update({ linkedList.end.data: linkedList.end })

                while tempNode.end != None:
                  linkedList.middle.update({ tempNode.data: tempNode })
                  tempNode = tempNode.end

                linkedList.end = tempNode

                tsp.remove(tempLinkedList)
                break
            # Edge is on the end of the newly created linked list
            else:
              # Node is on start of linkedList (No rerouting)
              if isEnd == False:
                tempNode = tempLinkedList.end
                tempNode.end = linkedList.start
                linkedList.start.start = tempLinkedList.end
                linkedList.middle.update({ linkedList.start.data: linkedList.start })

                while tempNode.start != None:
                  linkedList.middle.update({ tempNode.data: tempNode })
                  tempNode = tempNode.start
                
                linkedList.start = tempNode

                tsp.remove(tempLinkedList)
                break

              # Node is on end of linkedList (Requires rerouting)
              else:
                linkedList.end.end = tempLinkedList.end
                linkedList.middle.update({ linkedList.end.data: linkedList.end })

                tempPrevNode = linkedList.end
                tempNode = tempLinkedList.end 
                tempNextNode = tempLinkedList.end.start

                while tempNextNode != None:
                  linkedList.middle.update({ tempNode.data: tempNode })
                  tempNode.start = tempPrevNode
                  tempNode.end = tempNextNode
                  
                  tempPrevNode = tempNode
                  tempNode = tempNextNode
                  tempNextNode = tempNextNode.start

                tempNode.start = tempPrevNode
                tempNode.end = None
                linkedList.end = tempNode

                tsp.remove(tempLinkedList)
                break
        else:
          # Two linked lists don't need to be connected
          if tempLinkedList == None:
            endNode = Node(edge)
            endNode.start = node
            node.end = endNode

            newLinkedList = LinkedList(startNode, endNode)
            newLinkedList.middle.update({ node.data: node })

            tsp.append(newLinkedList)
            break

          # The newly created linked list needs to be connected
          #NOTE Only two nodes are involved and does not involve iteration rerouting 
          else:
            if edge == tempLinkedList.start.data:
              tempLinkedList.start.start = node
              node.end = tempLinkedList.start
              tempLinkedList.middle.update({ tempLinkedList.start.data: tempLinkedList.start })
              tempLinkedList.middle.update({ node.data: node })
              tempLinkedList.start = startNode
            elif edge == tempLinkedList.end.data:
              tempLinkedList.end.end = node
              node.start = tempLinkedList.end
              node.end = startNode
              startNode.start = node
              startNode.end = None
              tempLinkedList.middle.update({ tempLinkedList.end.data: tempLinkedList.end })
              tempLinkedList.middle.update({ node.data: node })
              tempLinkedList.end = startNode
            break
  
  ## The node is on an edge
  else:
    if DEBUG: print("Node is on edge")
    node = None
    endNode = None
    isEnd = False
    
    if v[NAME] == linkedList.start.data:
      node = linkedList.start
    elif v[NAME] == linkedList.end.data:
      node = linkedList.end
      isEnd = True

    for edge in v[EDGES]:
      if DEBUG: print("Edge:" + str(edge))
      if endNode != None:
        break
      isMiddle = False
      tempLinkedList = None
      for ll in tsp:
        if inMiddle(ll, edge):
          isMiddle = True
          break
        elif edge == ll.start.data or edge == ll.end.data:
          # Check if close off current loop when at end
          if ll == linkedList and len(linkedList.middle) + 2 < len(graph):
            isMiddle = True
            break
          tempLinkedList = ll
          break

      if isMiddle == True:
        continue

      # Two linked lists don't need to be connected
      #NOTE We are only dealing with one linked list
      if tempLinkedList == None:
        endNode = Node(edge)
        if isEnd == False:
          node.start = endNode
          endNode.end = node
          linkedList.middle.update({ node.data: node })
          linkedList.start = endNode
        else:
          node.end = endNode
          endNode.start = node
          linkedList.middle.update({ node.data: node })
          linkedList.end = endNode
        break
      # We are dealing with two, possibly large linked lists
      # We must merge them
      else:
        # Edge is on the start of the newly created linked list
        if edge == tempLinkedList.start.data:
          # Node is on start of linkedList (Requires rerouting)
          if isEnd == False:
            linkedList.start.start = tempLinkedList.start
            linkedList.middle.update({ linkedList.start.data: linkedList.start })

            tempPrevNode = linkedList.start
            tempNode = tempLinkedList.start
            tempNextNode = tempLinkedList.start.end

            while tempNextNode != None:
              linkedList.middle.update({ tempNode.data: tempNode })
              tempNode.start = tempNextNode
              tempNode.end = tempPrevNode
              
              tempPrevNode = tempNode
              tempNode = tempNextNode
              tempNextNode = tempNextNode.end

            tempNode.end = tempPrevNode
            tempNode.start = None
            linkedList.start = tempNode

            tsp.remove(tempLinkedList)

          # Node is on end of linkedList (No rerouting)
          else:
            tempNode = tempLinkedList.start
            tempNode.start = linkedList.end
            linkedList.end.end = tempLinkedList.start
            linkedList.middle.update({ linkedList.end.data: linkedList.end })

            while tempNode.end != None:
              linkedList.middle.update({ tempNode.data: tempNode })
              tempNode = tempNode.end

            linkedList.end = tempNode

            tsp.remove(tempLinkedList)
        # Edge is on the end of the newly created linked list
        else:
          # Node is on start of linkedList (No rerouting)
          if isEnd == False:
            tempNode = tempLinkedList.end
            tempNode.end = linkedList.start
            linkedList.start.start = tempLinkedList.end
            linkedList.middle.update({ linkedList.start.data: linkedList.start })

            while tempNode.start != None:
              linkedList.middle.update({ tempNode.data: tempNode })
              tempNode = tempNode.start
            
            linkedList.start = tempNode

            tsp.remove(tempLinkedList)

          # Node is on end of linkedList (Requires rerouting)
          else:
            linkedList.end.end = tempLinkedList.end
            linkedList.middle.update({ linkedList.end.data: linkedList.end })

            tempPrevNode = linkedList.end
            tempNode = tempLinkedList.end 
            tempNextNode = tempLinkedList.end.start

            while tempNextNode != None:
              linkedList.middle.update({ tempNode.data: tempNode })
              tempNode.start = tempPrevNode
              tempNode.end = tempNextNode
              
              tempPrevNode = tempNode
              tempNode = tempNextNode
              tempNextNode = tempNextNode.start

            tempNode.start = tempPrevNode
            tempNode.end = None
            linkedList.end = tempNode

            tsp.remove(tempLinkedList)
        break

  if DEBUG:
    print("================")
    for ll in tsp:
      printLL(ll)
    print()

if DEBUG:
  printLLFinal(tsp[0])
  print()

print("Minimum:" + str(getTot(tsp[0])))

printWithEdgeWeight(tsp[0])
