
## Checks in the vertices equal eachother in the end.
## Removed because algorithm should check for itself.
if curVert == numVert:
  for key, value in graphDict[tsp[FINAL_ARR]["start"]].items():
    if key == tsp[FINAL_ARR]["end"]:
      hPath = True
      break