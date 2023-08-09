import numpy as np

p = 0.6
a = np.array([4,3,3,2,1])

a = sorted(a, reverse=True)
n = sum(a)

def get_av(a, ix, k, n):
    """
    Gets the availablity percentage of a system where
    replicas are placed in pods, the replicas form a k-of-n system
    and the pods (racks) have some probability of failing. 
    Inputs:
        a: Array telling you how many replicas are in each pod (rack).
        ix: Just pass 0 to the function always.
        k: The number of replicas that should be up for the system to function.
    """
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

