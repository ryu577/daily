import numpy as np
from scipy.stats import binom


class VMAlloc():
    def __init__(self, m, m1):
        self.m = m
        self.m1 = m1
        self.n = len(m)
        self.constr_sum = 0
        self.maxs = []
        for i in range(self.n):
            self.maxs.append(int(m1/m[i]))
        self.pts = []

    def explore(self, lvl=0, arr=[]):
        if lvl >= self.n:
            print(arr)
            return
        for i in range(int(self.m1/self.m[lvl])+1):
            arr.append(i)
            self.explore(lvl+1, arr)
            arr.pop()

    def explore2(self, lvl=0, arr=[]):
        if self.constr_sum > self.m1:
            return
        elif lvl >= self.n:
            print(arr)
            self.pts.append(np.copy(arr))
            return
        for i in range(int(self.m1/self.m[lvl])+1):
            arr.append(i)
            self.constr_sum += i*self.m[lvl]
            self.explore2(lvl+1, arr)
            arr.pop()
            self.constr_sum -= i*self.m[lvl]


def binom_pmf(a=np.array([1, 1, 1]),
              maxs=np.array([3, 3, 3]),
              ps=np.array([.2, .3, .4])):
    prod1 = 1
    for i in range(len(a)):
        prod1 *= binom.pmf(a[i], maxs[i], ps[i])
    return prod1


def binom_sf(as1, maxs, ps):
    sum1 = 0
    for a in as1:
        sum1 += binom_pmf(a, maxs, ps)
    return sum1


if __name__ == "__main__":
    m = np.array([1.2, 1.9, 2.7, 2.2])
    m1 = 13
    c = np.array([1, 2, 3, 2])
    c1 = 8
    probs = np.array([.9, .8, .77, .84])

    vma = VMAlloc(m, m1)
    vma.explore2()

    print("################")
    vma1 = VMAlloc(c, c1)
    vma1.explore2()

    # Now get the best tuple of (n1, n2, n3).
    minn = 1
    winner = []
    for a1 in vma.pts:
        sum1 = binom_sf(vma1.pts, a1, probs)
        if sum1 < minn:
            minn = sum1
            winner = a1

    print("winner:")
    print(winner)
    print(minn)
