import numpy as np
from collections import Counter


def simulate_placement():
    sum1 = 0
    n_sim = 10000
    for ii in range(n_sim):
        num_racks = 5
        # Model for Shanim.. server as a fault domain.
        vmss_size = 5
        physical_fdgs = np.random.choice(np.arange(20),
                                        size = vmss_size,
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
