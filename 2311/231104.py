import numpy as np
import itertools


def permut_sign(a):
    """
    The sign of a permutation is simply the number of inversions.
    This is a simple, O(n^2) algorithm for finding the inversions. It can
    be done more efficiently with merge sort in O(n.log(n)) time.
    """
    cnt = 0
    for i in range(len(a)):
        for j in range(i+1, len(a)):
            if a[i] > a[j]:
                cnt += 1
    # Convert the 0-1 into -1 and +1
    return (cnt % 2 - .5) * -2


def leibniz_determinant(a):
    """
    Here, a is the matrix whose determinant we want to calculate.
    """
    n = len(a)
    arr = np.arange(n)
    determinant = 0
    for perm in itertools.permutations(arr):
        sign1 = permut_sign(perm)
        term = 1
        for i in range(len(perm)):
            j = int(perm[i])
            term = term * a[i, j]
        determinant += sign1 * term
    return determinant


a = np.array([[2, 1, 5],
              [4, 3, 1],
              [2, 2, 5]])

det1 = leibniz_determinant(a)
det2 = np.linalg.det(a)
print(abs(det1 - det2) <= 0.00001)
