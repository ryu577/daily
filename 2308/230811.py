import numpy as np
from scipy.stats import binom
from copy import deepcopy


# Original version in 230718w.
def get_av2(a, ix, k, p, q):
    """
    Gets the availability of a system with n racks.
    The array, a defines the number of nodes in each rack.
    p is the probability node will work (rack level failures).
    q is the probability vmss instance will work (node and VM failures).
    """
    pod = a[ix]
    n = sum(a[ix:])
    if k <= 0:
        return 1
    elif n < k:
        return 0
    elif ix == len(a) - 1:
        if k > pod:
            return 0
        else:
            return p
    a_1 = 0
    for jj in range(pod+1):
        a_1 += binom.pmf(jj, pod, q)*get_av2(a, ix+1, k-jj, p, q)
    a_0 = get_av2(a, ix+1, k, p, q)
    av = p*a_1 + (1-p)*a_0
    return av


def get_lmb(a, k, lmb, mu):
    p = mu/(lmb+mu)
    denom = 0
    for i in range(len(a)):
        replicas = a[i]
        a_1 = deepcopy(a)
        a_1.pop(i)
        denom = denom + get_av2(a_1, 0, k-replicas, p, 1) -\
                        get_av2(a_1, 0, k, p, 1)
    denom = denom*lmb*mu/(lmb+mu)
    av1 = get_av2(a, 0, k, p, 1)
    return denom/av1


def get_lmb2(a, k, lmb, mu, lmb1, mu1):
    p = mu/(lmb+mu)
    q = mu1/(lmb1+mu1)
    denom = 0
    for i in range(len(a)):
        replicas = a[i]
        a_1 = deepcopy(a)
        a_1.pop(i)
        denom = denom + get_av2(a_1, 0, k-replicas, p, q) -\
                        get_av2(a_1, 0, k, p, q)
    denom = denom*lmb*mu/(lmb+mu)
    denom1 = 0
    for i in range(len(a)):
        replicas = a[i]
        a_1 = deepcopy(a)
        a_1[i] -= 1
        denom1 = denom1 + replicas*(get_av2(a,0,k-1,p,q)-\
                                    get_av2(a_1,0,k,p,q))
    denom1 = denom1*lmb1*mu1/(lmb1+mu1)
    denom = denom + denom1
    av1 = get_av2(a, 0, k, p, q)
    return denom/av1

