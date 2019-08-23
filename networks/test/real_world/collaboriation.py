from networkx import read_gml
from networks.algorithms.clauset_newman_moore import clauset_newman_moore
from networks.algorithms.girvan_newman import girvan_newman
from networks.algorithms.hierarchical_clustering import hierarchical_clustering
from networks.algorithms.blondel import blondel
from time import time

#  Compiled by Mark Newman - refer to:
#  Newman, M. E. J. (2006). Finding community structure in networks using the
#  eigenvectors of matrices. Phys. Rev. E, 74:036104.
#  This network of 1589 nodes and 2742 edges reflects coauthorships between scientists
#  working in the area of network studies.


g = read_gml('data/netscience.gml', label='id')
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

