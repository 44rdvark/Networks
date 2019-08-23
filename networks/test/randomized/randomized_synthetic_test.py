from time import time
from networks.algorithms.clauset_newman_moore import clauset_newman_moore
from networks.common.modularity import get_modularity
from networks.common.partition_to_communities import get_partitioning
from networks.common.random_network import generate_synthetic_network
from networks.algorithms.girvan_newman import girvan_newman
from networks.algorithms.hierarchical_clustering import hierarchical_clustering
from networks.algorithms.blondel import blondel
from networks.common.evaluate_similarity import evaluate

# Tests run on networks generated in accordance with Girvan-Newman model - refer to:
# Girvan, M. and Newman, M. E. J. (2002). Community structure in social and biological
# networks. Proceedings of the National Academy of Sciences, 99(12):7821–7826.
# Tests compare the modularity and Rand index (calculated against the ground truth partition)
# of partitions returned by the algorithms as well as the algorithms' execution time.
# The four values below are parameters of the model - modifying them produces different networks

n_communities = 10
nodes_per_community = 10
probability_inner = 0.9  # probability of an edge between nodes in the same community
probability_outer = 0.1  # probability of an edge between nodes in different communities

nodes, edges, partitioning = generate_synthetic_network(10, 10, 0.9, 0.1)
start = time()
out, mod = blondel(nodes, edges)
end = time()
print("--- Blondel ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), partitioning), 2))

start = time()
out, mod = clauset_newman_moore(nodes, edges)
end = time()
print("\n--- Clauset-Newman-Moore ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), partitioning), 2))

start = time()
out, mod = hierarchical_clustering(nodes, edges)
end = time()
print("\n--- Hierarchical clustering ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), partitioning), 2))

start = time()
out, mod = girvan_newman(nodes, edges)
end = time()
print("\n--- Girvan-Newman ---")
print("modularity: ", round(mod, 2))
print("time: ", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), partitioning), 2))

print("\n--- Proper ---")

print("modularity: ", round(get_modularity(nodes, edges, partitioning), 2))