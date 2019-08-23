from time import time
from networks.clauset_newman_moore import clauset_newman_moore
from networks.common.partition_to_communities import get_partitioning
from networks.common.random_network import generate_social_network
from networks.girvan_newman import girvan_newman
from networks.hierarchical_clustering import hierarchical_clustering
from networks.blondel import blondel
from networks.common.evaluate_similarity import evaluate

line_nodes = [0, 1, 2, 3, 4]
line_adj_list = [set([1]), set([0, 2]), set([1, 3]), set([2, 4]), set([3])]
p_prim = [0.34, 0.33, 0.33]
p_sec = [0.0, 0.95, 0.05]

nodes, edges = generate_social_network(line_nodes, line_adj_list, 100000, p_prim, p_sec)
print(len(nodes), len(edges))
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
