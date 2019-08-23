from networkx import read_gml
from networks.clauset_newman_moore import clauset_newman_moore
from networks.common.display import display
from networks.common.evaluate_similarity import evaluate
from networks.common.modularity import get_modularity
from networks.common.partition_to_communities import get_partitioning
from networks.girvan_newman import girvan_newman
from networks.hierarchical_clustering import hierarchical_clustering
from networks.blondel import blondel
from time import time

g = read_gml('../data/football.gml', label='id')
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
print(round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))

start = time()
out, mod = clauset_newman_moore(nodes, edges)
end = time()
print("\n--- Clauset-Newman-Moore ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print(round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))


start = time()
out, mod = hierarchical_clustering(nodes, edges)
end = time()
print("\n--- Hierarchical clustering ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print(round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))

start = time()
out, mod = girvan_newman(nodes, edges)
end = time()
print("\n--- Girvan-Newman ---")
print("modularity: ", round(mod, 2))
print("time: ", round(end - start, 2))
print(round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))


print("\n--- Proper ---")

print("modularity: ", round(get_modularity(nodes, edges, get_partitioning(proper)), 2))
print(round(evaluate(get_partitioning(proper), get_partitioning(proper)), 2))




