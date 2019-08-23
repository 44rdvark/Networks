from math import sqrt
from statistics import stdev
from time import time

from networks.blondel_deg_dec import blondel_dec
from networks.blondel_deg_inc import blondel_inc
from networks.common.random_network import generate_social_network
from networks.blondel_randomized import blondel
import matplotlib.pyplot as plt


line_nodes = [0, 1, 2, 3, 4]
line_adj_list = [set([1]), set([0, 2]), set([1, 3]), set([2, 4]), set([3])]
p_prim = [0.34, 0.33, 0.33]
p_sec = [0.0, 0.95, 0.05]
datapoints = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
n_samples = 20
dev_t = []
dev_m = []
mean_t = []
mean_m = []
max_t = []
max_m = []
min_t = []
min_m = []
inc_t = []
dec_t = []
inc_m = []
dec_m = []
for point in datapoints:
    times = []
    mods = []
    nodes, edges = generate_social_network(line_nodes, line_adj_list, point, p_prim, p_sec)
    start = time()
    out, mod = blondel_dec(nodes, edges)
    end = time()
    dec_t.append(end - start)
    dec_m.append(mod)

    start = time()
    out, mod = blondel_inc(nodes, edges)
    end = time()
    inc_t.append(end - start)
    inc_m.append(mod)

    for i in range(n_samples):
        print(point, i)
        start = time()
        out, mod = blondel(nodes, edges)
        end = time()
        times.append(end - start)
        mods.append(mod)

    max_t.append(max(times))
    min_t.append(min(times))
    max_m.append(max(mods))
    min_m.append(min(mods))
    mean_t.append(sum(times) / len(times))
    mean_m.append(sum(mods) / len(mods))
    dev_t.append(stdev(times))
    dev_m.append(stdev(mods))

plt.plot(datapoints, min_t, '--ob', label="MIN")
plt.plot(datapoints, max_t, '--og', label="MAX")
plt.plot(datapoints, mean_t, '--or', label="MEAN")
plt.plot(datapoints, inc_t, '--oy', label="ASC")
plt.plot(datapoints, dec_t, '--ok', label="DES")


plt.legend()
plt.axis([10000, 100000, 0, 60])
plt.xlabel('Number of nodes')
plt.ylabel('Time')
plt.show()

plt.plot(datapoints, min_m, '--ob', label="MIN")
plt.plot(datapoints, max_m, '--og', label="MAX")
plt.plot(datapoints, mean_m, '--or', label="MEAN")
#plt.plot(datapoints, inc_m, '--oy', label="ASC")
#plt.plot(datapoints, dec_m, '--ok', label="DES")


plt.legend()
plt.axis([10000, 100000, 0.4, 0.6])
plt.xlabel('Number of nodes')
plt.ylabel('Modularity')
plt.show()

plt.plot(datapoints, [dev_t[i] / mean_t[i] for i in range(len(dev_t))], '--ok', label="CV")
plt.legend()
plt.axis([10000, 100000, 0, 0.5])
plt.xlabel('Number of nodes')
plt.ylabel('CV of time')
plt.show()

plt.plot(datapoints, dev_m, '--ok', label="SD")
plt.legend()
plt.axis([10000, 100000, 0, 0.01])
plt.xlabel('Number of nodes')
plt.ylabel('SD of modularity')
plt.show()
