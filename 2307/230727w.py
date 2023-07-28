import numpy as np
from collections import Counter


fd = np.arange(1, 91)

fdg = fd%20

rack = fd%5

spof = 0
for i in range(10000):
    fdgs = np.random.choice(fdg, size=5, replace=False)
    racks = rack[fdgs]
    arr = Counter(racks).values()
    if max(arr) > 2:
        spof += 1
print(spof/10000)

