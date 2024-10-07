import numpy as np


def matrix_chain(p, i, j, m):
    if i == j:
        return 0
    m[i, j] = np.inf
    for k in range(i, j):
        q = matrix_chain(p, i, k, m) + matrix_chain(p, k+1, j, m) +\
            p[i-1]*p[k]*p[j]
        if q < m[i, j]:
            m[i, j] = q
    return m[i, j]


def matrix_chain_memo(p):
    n = len(p) - 1
    m = np.ones((n+1, n+1))*np.inf
    return lookup_chain(m, p, 1, n)


def lookup_chain(m, p, i, j):
    if m[i, j] < np.inf:
        return m[i, j]
    if i == j:
        m[i, j] = 0
    else:
        for k in range(i, j):
            q = lookup_chain(m, p, i, k) + lookup_chain(m, p, k+1, j) +\
                p[i-1]*p[k]*p[j]
            if q < m[i, j]:
                m[i, j] = q
    return m[i, j]


# p = [10, 15, 5, 8, 12]
p = [30, 35, 15, 5, 10, 20, 25]
n = len(p) - 1
m = np.zeros((n+1, n+1))
mm = matrix_chain(p, 1, n, m)
print(m)p = [30, 35, 15, 5, 10, 20, 25]
n = len(p) - 1
m = np.zeros((n+1, n+1))
mm = matrix_chain(p, 1, n, m)
print(m)

