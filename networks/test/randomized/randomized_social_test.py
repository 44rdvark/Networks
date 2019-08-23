from time import time
from networks.algorithms.clauset_newman_moore import clauset_newman_moore
from networks.common.random_network import generate_social_network
from networks.algorithms.girvan_newman import girvan_newman
from networks.algorithms.hierarchical_clustering import hierarchical_clustering
from networks.algorithms.blondel import blondel

# Tests run on networks generated in accordance with social network model - refer to:
# Toivonen, R., Onnela, J.-P., Saramäki, J., Hyvönen, J., and Kaski, K. (2006).
# A model for social networks. Physica A Statistical Mechanics and its Applications,
# 371(2):851–860.
# Tests compare the modularity of partitions returned by the algorithms as well as
# the algorithms' execution time. The five variables below are parameters of the model.
# Modifying them produces different networks.


line_nodes = [0, 1, 2, 3, 4]  # nodes of the seed network
line_adj_list = [set([1]), set([0, 2]), set([1, 3]), set([2, 4]), set([3])]  # edges of the seed network
p_prim = [0.34, 0.33, 0.33]  # p_prim[i] - probability of adding i primary contacts - refer to the model
p_sec = [0.0, 0.95, 0.05]  # p_sec[i] - probability of adding i secondary contacts - refer to the model
n_nodes = 100  # number of nodes in the generated network

nodes, edges = generate_social_network(line_nodes, line_adj_list, n_nodes, p_prim, p_sec)
print("Number of nodes:", len(nodes), "\nNumber of edges:", len(edges))
start = time()
out, mod = blondel(nodes, edges)
end = time()
print("--- Blondel ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))

start = time()
out, mod = clauset_newman_moore(nodes, edges)
end = time()
print("\n--- Clauset-Newman-Moore ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))

start = time()
out, mod = hierarchical_clustering(nodes, edges)
end = time()
print("\n--- Hierarchical clustering ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))

start = time()
out, mod = girvan_newman(nodes, edges)
end = time()
print("\n--- Girvan-Newman ---")
print("modularity: ", round(mod, 2))
print("time: ", round(end - start, 2))
