import numpy as np

p = 0.6
a = np.array([4,3,3,2,1])

a = sorted(a, reverse=True)


def get_av(a, ix, k, n):
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

