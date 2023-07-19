import numpy as np
import pyray.shapes.fourd.tesseract_graph as tg
from itertools import combinations


# Check that an adjacency list is a valid mesh.
tf = tg.TsrctFcGraph(angle=np.pi/2)
tf.dfs_flatten2('00-+')
tf.reset_vert_col()
tf.actually_flatten()
tf.mk_xy_set()


if len(tf.xy_set) == 24:
    print("valid mesh")
else:
    print("invalid mesh")


# Get the adjacency list
for i in range(32):
    for j in range(3):
        for k in combinations(np.arange(32),23):
            print("comb")

## Nothing to see here. Check 230714 instead.
# Choosing an i and j (32*3) vs choosing a j for each i (3^32).
