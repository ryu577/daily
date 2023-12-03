import numpy as np
from scipy.special import comb


def comb_term3(i, j, k):
    n = 2*(i+j+k)
    prod = 1
    u, v, w = i, j, k
    while n > 0:
        prod = prod*n/max(i, j, k, u, v, w)
        n = n - 1
        if i == max(i, j, k, u, v, w):
            i = i - 1
        elif j == max(i, j, k, u, v, w):
            j = j - 1
        elif k == max(i, j, k, u, v, w):
            k = k - 1
        elif u == max(i, j, k, u, v, w):
            u = u - 1
        elif v == max(i, j, k, u, v, w):
            v = v - 1
        elif w == max(i, j, k, u, v, w):
            w = w - 1
    return prod


def comb_term2(i, j):
    n = 2*(i+j)
    prod = 1
    u, v = i, j
    while n > 0:
        prod = prod*n/max(i, j, u, v)
        n = n - 1
        if i == max(i, j, u, v):
            i = i - 1
        elif j == max(i, j, u, v):
            j = j - 1
        elif u == max(i, j, u, v):
            u = u - 1
        elif v == max(i, j, u, v):
            v = v - 1
    return prod


def sum_terms3(n=3):
    summ = 0
    for i in range(n+1):
        for j in range(n+1):
            if i + j <= n:
                k = n - i - j
                summ = summ + comb_term3(i, j, k)/36**n
    return summ


def sum_terms2(n=3):
    summ = 0
    for i in range(n+1):
        j = n-i
        summ = summ + comb_term2(i, j)/16**n
    return summ


def sim_3d(n=3):
    hits = 0
    for i in range(100000):
        strt = np.array([0, 0, 0])
        for ii in range(2*n):
            k = np.random.choice(3)
            strt[k] = strt[k] + np.random.choice([1, -1])
        if strt[0] == 0 and strt[1] == 0 and strt[2] == 0:
            hits = hits + 1
    return hits/100000


def sim_2d(n=3):
    hits = 0
    for i in range(10000):
        strt = np.array([0, 0])
        for ii in range(2*n):
            k = np.random.choice(2)
            strt[k] = strt[k] + np.random.choice([1, -1])
        if strt[0] == 0 and strt[1] == 0:
            hits = hits + 1
    return hits/10000


def sum_n(n=3):
    summ = 0
    for i in range(n):
        summ = summ + comb(n,i)**2*comb(2*(n-i),(n-i))
    return summ


if __name__ == "__main__":
    n = 3
    summ = sum_terms3(n)
    print(summ)
    summ1 = comb(2*n, n)**3/36**n
    print(summ1)
    summ2 = sum_terms2(n)
    print(summ2)
    summ3 = comb(2*n, n)**2/16**n
    print(summ3)
    prob3 = sim_3d()
    print(prob3)
    prob2 = sim_2d()
    print(prob2)
