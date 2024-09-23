from collections import Counter
from numpy import ceil, floor
import numpy as np


def g1(start, end, v, t):
    if t % 2 == 0:
        x = (2*end+3*start)//5
    else:
        x = (3*end+2*start)//5
    if x == v:
        return t+1
    elif v < x:
        return g1(start, x-1, v, t+1)
    else:
        return g1(x+1, end, v, t+1)


def g2(start, end, v, t):
    if t == 0:
        #x = np.random.randint(40, 60)
        x = 65
    elif t % 2 == 0:
        x = int(ceil((1*end+1*start)/2))
    else:
        x = int(floor((1*end+1*start)/2))
    if x == v:
        return t+1
    elif v < x:
        return g2(start, x-1, v, t+1)
    else:
        return g2(x+1, end, v, t+1)


def ex(turns):
    return 6 - turns


pays = [6-g2(1, 100, x, 0) for x in range(1, 101)]
print(sum(pays))
print(Counter(pays))

danger = [2,5,8,11,14,17,20,22,24,27,30,33,36,39,42,45,47,49,52,55,58,61,64,67,70,72,74,77,80,83,85,87,90,93,96,98,100]
