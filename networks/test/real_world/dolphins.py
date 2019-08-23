from networkx import read_gml
from networks.algorithms.clauset_newman_moore import clauset_newman_moore
from networks.algorithms.girvan_newman import girvan_newman
from networks.algorithms.hierarchical_clustering import hierarchical_clustering
from networks.algorithms.blondel import blondel
from time import time

#  The network of bottlenose dolphins was assembled and studied by Lusseau et al. - refer to
#  Lusseau, D., Schneider, K., Boisseau, O., Haase, P., Slooten, E., and Dawson,
#  S. (2003). The bottlenose dolphin community of doubtful sound features a large
#  proportion of long-lasting associations - can geographic isolation explain this unique
#  trait? Behavioral Ecology and Sociobiology, 54:396–405.
#  The particular group of dolphins exhibited exceptionally strong and long lasting connections
#  which are reflected by edges of the network. There are 62 nodes and 159 edges in total.

g = read_gml('data/dolphins.gml', label='id')
nodes = list(g.nodes())
edges = list(g.edges())

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

