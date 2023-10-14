import numpy as np
from stochproc.birth_death_processes.reliability.k_of_n import k_of_n_av


nodes = 64
replica_sets = 8
replicas = 7
p = 0.2
cnt = 0
n_sim = 50000

for ii in range(n_sim):
    a = np.zeros((nodes, replica_sets))
    for i in range(replica_sets):
        ixs = np.random.choice(np.arange(nodes), replicas, replace=False)
        a[ixs, i] = 1

    ps = [np.random.uniform() < p for i in range(nodes)]
    a1 = a[np.array(ps) == 1]
    sums = np.sum(a1, axis=0)
    if max(sums) > 3:
        cnt += 1

print(cnt/n_sim)
print(k_of_n_av(4, 7, .2))
