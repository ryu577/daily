import numpy as np
from collections import Counter
import ast


class Sys():
    def __init__(self, a, p=0.6):
        self.p = p
        #a = np.array([4,3,3,2,1])
        self.a = sorted(a, reverse=True)
        self.av_del = np.zeros(len(self.a))
        self.n = sum(a)

    def get_av(self, ix, k, n=None):
        if n is None:
            n = self.n
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
        a_1 = self.get_av(ix+1, k-pod, self.n-pod)
        a_0 = self.get_av(ix+1, k, self.n-pod)
        self.av_del[ix] = (a_1 - a_0)
        av = self.p*a_1 + (1-self.p)*a_0
        return av


##################
class VmssPerf():
    def __init__(self, vmss_size=5, p_rack=.99998):
        fd = np.arange(1, 91)
        self.fdg = fd % 20
        self.rack = fd % 5
        self.p_rack = p_rack
        self.vmss_size = vmss_size
        self.aa = {}

    def run_sim(self, n_sim=10000):
        spof = 0
        self.n_sim = n_sim
        for i in range(n_sim):
            fdgs = np.random.choice(np.arange(19),
                                    size=self.vmss_size,
                                    replace=False)
            racks = self.rack[fdgs]
            arr = Counter(racks).values()
            if max(arr) > self.vmss_size//2:
                spof += 1
            arr = sorted(arr, reverse=True)
            if str(arr) in self.aa:
                self.aa[str(arr)] += 1
            else:
                self.aa[str(arr)] = 1
        return spof/n_sim

    def get_sys_characteristics(self):
        av = 0
        for kk in self.aa.keys():
            prcnt = self.aa[kk]/self.n_sim
            arr = ast.literal_eval(kk)
            sys = Sys(arr, self.p_rack)
            av1 = sys.get_av(0, 3)
            av += av1*prcnt
        return av


def tst(vmss_size=5, p_rack=.99998):
    vp = VmssPerf(vmss_size, p_rack)
    vp.run_sim()
    vmss_av = vp.get_sys_characteristics()
    print(vmss_av)
