class Node:
  def __init__(self, data: int, name: int):
    self.data: int = data
    self.name: int = name
    self.start: Node = None
    self.end: Node = None

for i in range(0, 5):

  if i == 2:
    break

  for j in range(0, 5):
    if i == 0:
      break
      
    print(i)
