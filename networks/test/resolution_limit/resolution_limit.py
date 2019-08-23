from time import time
from networks.algorithms.clauset_newman_moore import clauset_newman_moore
from networks.common.clique_network import generate_clique_network
from networks.common.modularity import get_modularity
from networks.common.partition_to_communities import get_partitioning
from networks.algorithms.girvan_newman import girvan_newman
from networks.algorithms.hierarchical_clustering import hierarchical_clustering
from networks.algorithms.blondel import blondel
from networks.common.evaluate_similarity import evaluate

#  This program exemplifies the existence of a so called resolution limit. It is known for
#  modularity maximization algorithms to be unable to detect sufficiently small communities
#  regardless of how pronounced they are.
#  The algorithms are run on a network of 30 cliques each of size 5 connected to one another by
#  only singular edges. Despite the visible community structure of the network, the algorithms
#  fail to detect it, as evidenced by how the number of communities found by each of them differs
#  from the actual number.

nodes, edges, partitioning = generate_clique_network(5, 30)
start = time()
out, mod = blondel(nodes, edges)
end = time()
print("--- Blondel ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), partitioning), 2))
print("Number of communities:", len(out))

start = time()
out, mod = clauset_newman_moore(nodes, edges)
end = time()
print("\n--- Clauset-Newman-Moore ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), partitioning), 2))
print("Number of communities:", len(out))


start = time()
out, mod = hierarchical_clustering(nodes, edges)
end = time()
print("\n--- Hierarchical clustering ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), partitioning), 2))
print("Number of communities:", len(out))


start = time()
out, mod = girvan_newman(nodes, edges)
end = time()
print("\n--- Girvan-Newman ---")
print("modularity: ", round(mod, 2))
print("time: ", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), partitioning), 2))
print("Number of communities:", len(out))


print("\n--- Proper ---")
print("modularity: ", round(get_modularity(nodes, edges, partitioning), 2))
print("Rand index:", round(evaluate(partitioning, partitioning), 2))
print("Number of communities:", 30)


