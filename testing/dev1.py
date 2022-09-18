import numpy as np

FILENAME: str = "gen-graph.txt"

nums = np.loadtxt(FILENAME, dtype="i", delimiter=" ")

# Input Matrix
graph = [[j for j in vert] for vert in nums]


