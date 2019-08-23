from time import time
from networks.clauset_newman_moore import clauset_newman_moore
from networks.common.partition_to_communities import get_partitioning
from networks.common.random_network import generate_social_network
from networks.girvan_newman import girvan_newman
from networks.hierarchical_clustering import hierarchical_clustering
from networks.blondel import blondel
from networks.common.evaluate_similarity import evaluate
import matplotlib.pyplot as plt


line_nodes = [0, 1, 2, 3, 4]
line_adj_list = [set([1]), set([0, 2]), set([1, 3]), set([2, 4]), set([3])]
p_prim = [0.34, 0.33, 0.33]
p_sec = [0.0, 0.95, 0.05]
x_blo = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]
x_cnm = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]
x_gn = [100, 200, 300, 400]
x_hc = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]
yt_blo = []
yt_cnm = []
yt_gn = []
yt_hc = []
ym_blo = []
ym_cnm = []
ym_gn = []
ym_hc = []
n_datapoints = len(x_blo)
datapoints = x_blo
for i in range(len(x_blo)):
    nodes, edges = generate_social_network(line_nodes, line_adj_list, datapoints[i], p_prim, p_sec)
    print(len(nodes), len(edges))
    print("--- START ---")
    if i < len(x_blo):
        start = time()
        out, mod = blondel(nodes, edges)
        end = time()
        yt_blo.append(end - start)
        ym_blo.append(mod)

    print("Blo done")

    if i < len(x_cnm):
        start = time()
        out, mod = clauset_newman_moore(nodes, edges)
        end = time()
        yt_cnm.append(end - start)
        ym_cnm.append(mod)

    print("CNM done")

    if i < len(x_hc):
        start = time()
        out, mod = hierarchical_clustering(nodes, edges)
        end = time()
        yt_hc.append(end - start)
        ym_hc.append(mod)

    print("Hc done")

    if i < len(x_gn):
        start = time()
        out, mod = girvan_newman(nodes, edges)
        end = time()
        yt_gn.append(end - start)
        ym_gn.append(mod)

    print("GN done")

plt.plot(x_blo, yt_blo, '--ob', label="Blo")
plt.plot(x_cnm, yt_cnm, '--og', label="CNM")
plt.plot(x_gn, yt_gn, '--or', label="GN")
plt.plot(x_hc, yt_hc, '--oy', label="Hc")

plt.legend()
plt.axis([100, 1200, 0, 60])
plt.xlabel('Number of nodes')
plt.ylabel('Time (seconds)')
plt.show()

plt.plot(x_blo, ym_blo, '--ob', label="Blo")
plt.plot(x_cnm, ym_cnm, '--og', label="CNM")
plt.plot(x_gn, ym_gn, '--or', label="GN")
plt.plot(x_hc, ym_hc, '--oy', label="Hc")

plt.legend()
plt.axis([100, 1200, 0, 1])
plt.xlabel('Number of nodes')
plt.ylabel('Modularity')
plt.show()