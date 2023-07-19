import numpy as np
from collections import Counter
from scipy.stats import binom


def simulate_placement():
    sum1 = 0
    n_sim = 10000
    for ii in range(n_sim):
        num_racks = 5
        # Model for Shanim.. server as a fault domain.
        vmss_size = 5
        physical_fdgs = np.random.choice(np.arange(20),
                                         size=vmss_size,
                                         replace=False)
        physical_fd = []
        racks = []
        for fdg in physical_fdgs:
            fd = np.random.choice(5)*16 + fdg
            physical_fd.append(fd)
            racks.append(fd % num_racks)

        if max(Counter(racks).values()) > vmss_size//3+1:
            sum1 += 1

    print(sum1/n_sim)


# Model for discounting databricks.

sla = .997
n = 40
p = 0.0527293873732649

n1 = n
sf = binom.sf(n-1, n1, p)
while sf < sla:
    n1 += 1
    sf = binom.sf(n-1, n1, p)

discnt_fctr = n/n1
print(discnt_fctr)
