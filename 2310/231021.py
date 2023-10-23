import numpy as np
from stochproc.birth_death_processes.reliability.k_of_n import k_of_n_av


nodes = 4
replica_sets = 10
replicas = 3
# Probability node will go down.
p = 0.4

# Simulation parameters.
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
    if max(sums) > replicas//2:
        cnt += 1

print(1-cnt/n_sim)
print(k_of_n_av(replicas//2+1, replicas, 1-p))
