import numpy as np


lmb = 3
mu = 10
t1 = 0
t2 = 0
cache_miss = 0
req = 0
while t1 < 50000:
    req += 1
    if t1 > t2:
        t2 = t1+np.random.exponential(1/mu)
    t1 = t1+np.random.exponential(1/lmb)
    if t1 < t2:
        cache_miss += 1

print(cache_miss/req)

#####################


def state_p(lmb, mu, k):
    term = 1
    summ = 0
    for kk in range(k):
        summ += term
        term = term*lmb/(kk+1)/mu
    return term/(summ+term)


# Now with larger cache.
import heapq

lmb = 3
mu = 10
k = 2

t1 = 0
t2 = 0

req = 0
cache_miss = 0

arr = []
heapq.heapify(arr)
while t1 < 50000:
    req += 1
    if len(arr) < k:
        t2 = t1+np.random.exponential(1/mu)
        heapq.heappush(arr, t2)
    t1 = t1+np.random.exponential(1/lmb)
    if len(arr) == k:
        if arr[0] > t1:
            cache_miss += 1
        else:
            while len(arr) > 0 and arr[0] < t1:
                heapq.heappop(arr)

print(cache_miss/req)

####
# Order statistics of exponential.
# Say we ask for o VMs and need n.


def order_stats_time(o=80, n=40):
    term = o
    summ = 0
    for i in range(n):
        summ += 1/term
        term -= 1
    return summ
