import numpy as np


def matr_chain_order(p):
    n = len(p) - 1
    m = np.zeros(shape=((n+1), (n+1)))
    for l1 in range(2, n+1):
        for i in range(1, n-l1+1):
            j = i + l1 - 1
            m[i, j] = np.inf
            for k in range(1, j):
                q = m[i, j] + m[k+1, j] + p[i-1]*p[k]*p[j]
                if q < m[i, j]:
                    m[i, j] = q
    return m


def tst1():
    p = [5, 9, 10, 100, 5, 4]
    mm = matr_chain_order(p)
    print(mm)


def __init__():
    tst1()
