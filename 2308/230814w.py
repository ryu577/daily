import numpy as np
from collections import Counter
from scipy.stats import binom
from copy import deepcopy
import ast


# Original version in 230718w.
def get_av2(a, ix, k, p, q):
    """
    Gets the availability of a system with n racks.
    The array, a defines the number of nodes in each rack.
    p is the probability node will work (rack level failures).
    q is the probability vmss instance will work (node and VM failures).
    """
    pod = a[ix]
    n = sum(a[ix:])
    if k <= 0:
        return 1
    elif n < k:
        return 0
    elif ix == len(a) - 1:
        if k > pod:
            return 0
        else:
            return p
    a_1 = 0
    for jj in range(pod+1):
        a_1 += binom.pmf(jj, pod, q)*get_av2(a, ix+1, k-jj, p, q)
    a_0 = get_av2(a, ix+1, k, p, q)
    av = p*a_1 + (1-p)*a_0
    return av


def get_lmb2(a, k, lmb, mu, lmb1, mu1):
    p = mu/(lmb+mu)
    q = mu1/(lmb1+mu1)
    denom = 0
    for i in range(len(a)):
        replicas = a[i]
        a_1 = deepcopy(a)
        a_1.pop(i)
        denom = denom + get_av2(a_1, 0, k-replicas, p, q) -\
         get_av2(a_1, 0, k, p, q)
    denom = denom*lmb*mu/(lmb+mu)
    denom1 = 0
    for i in range(len(a)):
        replicas = a[i]
        a_1 = deepcopy(a)
        a_1[i] -= 1
        denom1 = denom1 + replicas * (get_av2(a, 0, k-1, p, q) -
                                      get_av2(a_1, 0, k, p, q))
    denom1 = denom1*lmb1*mu1/(lmb1+mu1)
    denom = denom + denom1
    av1 = get_av2(a, 0, k, p, q)
    return denom/av1


class Sys():
    def __init__(self, a, p=0.6, q=0.9):
        self.p = p
        self.q = q
        self.a = sorted(a, reverse=True)
        self.av_del = np.zeros(len(self.a))
        self.n = sum(a)

    def get_av(self, k, n=None):
        if n is None:
            n = self.n
        av = get_av2(self.a, 0, k, self.p, self.q)
        return av


##################
class VmssPerf():
    def __init__(self, vmss_size=5, p_rack=.99998, p_vm=0.9998):
        fd = np.arange(1, 91)
        self.fdg = fd % 20
        self.rack = fd % 5
        self.p_rack = p_rack
        self.p_vm = p_vm
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
            sys = Sys(arr, self.p_rack, self.p_vm)
            av1 = sys.get_av(self.vmss_size//2+1, self.vmss_size)
            av += av1*prcnt
        return av


def tst(vmss_size=5, p_rack=0.9999746, p_vm=0.99998):
    vp = VmssPerf(vmss_size, p_rack, p_vm)
    vp.run_sim()
    vmss_av = vp.get_sys_characteristics()
    print(vmss_av)
    print(vp.aa)
