import numpy as np
from collections import Counter
from collections import defaultdict
import ast

fd = np.arange(1, 91)

fdg = fd%20

rack = fd%5
aa = {}

spof = 0
n_sim = 10000
for i in range(n_sim):
    fdgs = np.random.choice(fdg, size=5, replace=False)
    racks = rack[fdgs]
    arr = Counter(racks).values()
    if max(arr) > 2:
        spof += 1
    arr = sorted(arr, reverse=True)
    if str(arr) in aa:
        aa[str(arr)] += 1
    else:
        aa[str(arr)] = 1
print(spof/n_sim)

for kk in aa.keys():
    arr = ast.literal_eval(kk)
    av1 = get_av(arr, 0, 3)

#########################
p = 0.6
a = np.array([4,3,3,2,1])

a = sorted(a, reverse=True)
n = sum(a)

# Original version in 230718w.
def get_av(a, ix, k):
    pod = a[ix]
    if k <= 0:
        return 1
    elif sum(a[ix:]) < k:
        return 0
    elif ix == len(a) - 1:
        if k < pod:
            return 0
        else:
            return p
    av = p*get_av(a, ix+1, k-pod, n-pod) +\
        (1-p)*get_av(a, ix+1, k, n-pod)
    return av
