import numpy as np
from scipy.stats import binom


def est_n(sla=.997, n=40, p=0.0527293873732649):
    n1 = n
    sf = binom.sf(n-1, n1, p)
    while sf < sla:
        n1 += 1
        sf = binom.sf(n-1, n1, p)
    return n1


n = 40
n1 = est_n(n=n)
n2 = est_n(n=n, sla=.997, p=.99)
discnt_fctr = 1-n2/n1
print(discnt_fctr)

