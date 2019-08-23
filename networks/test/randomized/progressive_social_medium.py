from time import time
from networks.algorithms.clauset_newman_moore import clauset_newman_moore
from networks.common.random_network import generate_social_network
from networks.algorithms.blondel import blondel
import matplotlib.pyplot as plt

# Tests run on progressively larger (between 1000 and 10000 nodes) networks
# generated in accordance with social network model - refer to:
# Toivonen, R., Onnela, J.-P., Saramäki, J., Hyvönen, J., and Kaski, K. (2006).
# A model for social networks. Physica A Statistical Mechanics and its Applications,
# 371(2):851–860.
# The program displays plots showcasing how different algorithms compare in terms of modularity
# of partitions detected and execution time.

line_nodes = [0, 1, 2, 3, 4]
line_adj_list = [set([1]), set([0, 2]), set([1, 3]), set([2, 4]), set([3])]
p_prim = [0.34, 0.33, 0.33]
p_sec = [0.0, 0.95, 0.05]
x_blo = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
x_cnm = [1000, 2000, 3000, 4000, 5000, 6000, 7000]
yt_blo = []
yt_cnm = []
ym_blo = []
ym_cnm = []
n_datapoints = len(x_blo)
datapoints = x_blo
for i in range(len(x_blo)):
    nodes, edges = generate_social_network(line_nodes, line_adj_list, datapoints[i], p_prim, p_sec)
    print("Number of nodes:", len(nodes), "\nNumber of edges:", len(edges))
    if i < len(x_blo):
        start = time()
        out, mod = blondel(nodes, edges)
        end = time()
        yt_blo.append(end - start)
        ym_blo.append(mod)

    if i < len(x_cnm):
        start = time()
        out, mod = clauset_newman_moore(nodes, edges)
        end = time()
        yt_cnm.append(end - start)
        ym_cnm.append(mod)

plt.plot(x_blo, yt_blo, '--ob', label="Blo")
plt.plot(x_cnm, yt_cnm, '--og', label="CNM")


plt.legend()
plt.axis([1000, 10000, 0, 60])
plt.xlabel('Number of nodes')
plt.ylabel('Time (seconds)')
plt.show()

plt.plot(x_blo, ym_blo, '--ob', label="Blo")
plt.plot(x_cnm, ym_cnm, '--og', label="CNM")


plt.legend()
plt.axis([1000, 10000, 0, 1])
plt.xlabel('Number of nodes')
plt.ylabel('Modularity')
plt.show()