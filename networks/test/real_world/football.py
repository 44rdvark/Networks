from networkx import read_gml
from networks.algorithms.clauset_newman_moore import clauset_newman_moore
from networks.common.evaluate_similarity import evaluate
from networks.common.modularity import get_modularity
from networks.common.partition_to_communities import get_partitioning
from networks.algorithms.girvan_newman import girvan_newman
from networks.algorithms.hierarchical_clustering import hierarchical_clustering
from networks.algorithms.blondel import blondel
from time import time

#  The network was assembled by Girvan and Newman - refer to:
#  Girvan, M. and Newman, M. E. J. (2002). Community structure in social and biological
#  networks. Proceedings of the National Academy of Sciences, 99(12):7821–7826.
#  It reflects the schedule of American College football league in year 2000.
#  Nodes correspond to teams while an edge exists between two vertices if the teams they
#  represent played a game together during the season. Importantly, teams are separated
#  into conferences based on geographical proximity and games between teams in the same
#  conference are more frequent that games between those from different divisions.
#  Thus, a ground truth community partition corresponds to the conference structure of the
#  league. There are 115 nodes, 613 edges and 12 ground truth communities in the network.


g = read_gml('data/football.gml', label='id')
d = dict(g.nodes(data="value"))
proper = [[] for _ in range(12)]
for node, com in d.items():
    proper[com].append(node)

nodes = list(g.nodes())
edges = list(g.edges())
start = time()
out, mod = blondel(nodes, edges)
end = time()
print("--- Blondel ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))

start = time()
out, mod = clauset_newman_moore(nodes, edges)
end = time()
print("\n--- Clauset-Newman-Moore ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))


start = time()
out, mod = hierarchical_clustering(nodes, edges)
end = time()
print("\n--- Hierarchical clustering ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))

start = time()
out, mod = girvan_newman(nodes, edges)
end = time()
print("\n--- Girvan-Newman ---")
print("modularity: ", round(mod, 2))
print("time:", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))


print("\n--- Proper ---")

print("modularity: ", round(get_modularity(nodes, edges, get_partitioning(proper)), 2))



