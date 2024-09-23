import numpy as np


def matr_chain_order(p):
    n = len(p) - 1
    m = np.zeros(shape=((n+1), (n+1)))
    s = np.zeros(shape=((n+1), (n+1)))
    for l1 in range(2, n+1):
        for i in range(1, n-l1+1+1):
            j = i + l1 - 1
            m[i, j] = np.inf
            for k in range(i, j):
                q = m[i, k] + m[k+1, j] + p[i-1]*p[k]*p[j]
                if q < m[i, j]:
                    m[i, j] = q
                    s[i, j] = k
    return m, s


def tst1():
    # p = [5, 9, 10, 100, 5, 4]
    p = [30, 35, 15, 5, 10, 20, 25]
    mm, ss = matr_chain_order(p)
    ss = ss.astype(int)
    print(mm)
    print(ss)
    print_opt_paren(ss, 1, 6)


def print_opt_paren(s, i, j):
    if i == j:
        print("A"+str(i)+".", end='')
    else:
        print("(", end='')
        print_opt_paren(s, i, int(s[i][j]))
        print_opt_paren(s, int(s[i][j]+1), j)
        print(")", end='')


if __name__ == "__main__":
    tst1()
