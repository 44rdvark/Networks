from time import time
from networks.clauset_newman_moore import clauset_newman_moore
from networks.common.modularity import get_modularity
from networks.common.partition_to_communities import get_partitioning
from networks.common.random_network import generate_synthetic_network
from networks.girvan_newman import girvan_newman
from networks.hierarchical_clustering import hierarchical_clustering
from networks.blondel import blondel
from networks.common.evaluate_similarity import evaluate


nodes, edges, partitioning = generate_synthetic_network(10, 10, 0.9, 0.1)
print(len(nodes), len(edges))
start = time()
out, mod = blondel(nodes, edges)
end = time()
print("--- Blondel ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
print(round(evaluate(get_partitioning(out), partitioning), 2))



start = time()
out, mod = clauset_newman_moore(nodes, edges)
end = time()
print("\n--- Clauset-Newman-Moore ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print(round(evaluate(get_partitioning(out), partitioning), 2))

start = time()
out, mod = hierarchical_clustering(nodes, edges)
end = time()
print("\n--- Hierarchical clustering ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print(round(evaluate(get_partitioning(out), partitioning), 2))

start = time()
out, mod = girvan_newman(nodes, edges)
end = time()
print("\n--- Girvan-Newman ---")
print("modularity: ", round(mod, 2))
print("time: ", round(end - start, 2))
print(round(evaluate(get_partitioning(out), partitioning), 2))

print("\n--- Proper ---")

print("modularity: ", round(get_modularity(nodes, edges, partitioning), 2))
print(round(evaluate(partitioning, partitioning), 2))