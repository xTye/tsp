for edge in v[EDGES]:
    for ll in tsp:
    if inMiddle(ll, edge):
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

    if node == True:
    break