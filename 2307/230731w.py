import numpy as np
from collections import Counter
import ast


class Sys():
    def __init__(self, a):
        self.p = 0.6
        #a = np.array([4,3,3,2,1])
        self.a = sorted(a, reverse=True)
        self.av_del = np.zeros(len(self.a))
        self.n = sum(a)

    def get_av(self, ix, k):
        pod = self.a[ix]
        if k <= 0:
            return 1
        elif sum(self.a[ix:]) < k:
            return 0
        elif ix == len(self.a) - 1:
            if k < pod:
                return 0
            else:
                return self.p
        a_1 = self.get_av(self.a, ix+1, k-pod, self.n-pod)
        a_0 = self.get_av(self.a, ix+1, k, self.n-pod)
        self.av_del[ix] = (a_1 - a_0)
        av = self.p*a_1 + (1-self.p)*a_0
        return av


##################
class VmssPerf():
    def __init__(self, vmss_size=5):
        fd = np.arange(1, 91)
        self.fdg = fd%20
        self.rack = fd%5
        self.aa = {}

    def run_sim(self, n_sim=10000):
        spof = 0
        self.n_sim = n_sim
        for i in range(n_sim):
            fdgs = np.random.choice(self.fdg, size=5, replace=False)
            racks = self.rack[fdgs]
            arr = Counter(racks).values()
            if max(arr) > 2:
                spof += 1
            arr = sorted(arr, reverse=True)
            if str(arr) in self.aa:
                self.aa[str(arr)] += 1
            else:
                self.aa[str(arr)] = 1
        print(spof/n_sim)

    def get_sys_characteristics(self):
        for kk in self.aa.keys():
            prcnt = self.aa[kk]/self.n_sim
            arr = ast.literal_eval(kk)
            sys = Sys(arr)
            av1 = sys.get_av(0, 3)
