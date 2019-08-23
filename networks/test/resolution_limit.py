from time import time

import networkx as nx

from networks.clauset_newman_moore import clauset_newman_moore
from networks.common.clique_network import generate_clique_network
from networks.common.display import display
from networks.common.modularity import get_modularity
from networks.common.partition_to_communities import get_partitioning
from networks.common.random_network import generate_synthetic_network
from networks.girvan_newman import girvan_newman
from networks.hierarchical_clustering import hierarchical_clustering
from networks.blondel import blondel
from networks.common.evaluate_similarity import evaluate
import matplotlib.pyplot as plt


nodes, edges, partitioning = generate_clique_network(5, 30)
print(len(edges))
print(edges)
start = time()
out, mod = blondel(nodes, edges)
end = time()
print("--- Blondel ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
print(len(out))
print(round(evaluate(get_partitioning(out), partitioning), 2))


start = time()
out, mod = clauset_newman_moore(nodes, edges)
end = time()
print("\n--- Clauset-Newman-Moore ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print(len(out))
print(out)
print(round(evaluate(get_partitioning(out), partitioning), 2))


start = time()
out, mod = hierarchical_clustering(nodes, edges)
end = time()
print("\n--- Hierarchical clustering ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print(len(out))
print(round(evaluate(get_partitioning(out), partitioning), 2))
print(out)
#display(nodes, edges, out)


start = time()
out, mod = girvan_newman(nodes, edges)
end = time()
print("\n--- Girvan-Newman ---")
print("modularity: ", round(mod, 2))
print("time: ", round(end - start, 2))
print(len(out))
print(out)
print(round(evaluate(get_partitioning(out), partitioning), 2))


print("\n--- Proper ---")
print("modularity: ", round(get_modularity(nodes, edges, partitioning), 2))
print(round(evaluate(partitioning, partitioning), 2))


