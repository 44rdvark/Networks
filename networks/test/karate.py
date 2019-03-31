from networkx import read_gml
from networks.clauset_newman_moore import clauset_newman_moore
from networks.common.display import display
from networks.girvan_newman import girvan_newman
from networks.hierarchical_clustering import hierarchical_clustering
from networks.blondel import blondel
from time import time

g = read_gml('../data/karate.gml', label='id')
nodes = list(g.nodes())
edges = list(g.edges())
for i in range(len(nodes)):
    nodes[i] = nodes[i] - 1
for i in range(len(edges)):
    edges[i] = (edges[i][0] - 1, edges[i][1] - 1)

start = time()
out, mod = blondel(nodes, edges)
end = time()
print("--- Blondel ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
display(nodes, edges, out)

start = time()
out, mod = clauset_newman_moore(nodes, edges)
end = time()
print("\n--- Clauset-Newman-Moore ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
display(nodes, edges, out)


start = time()
out, mod = hierarchical_clustering(nodes, edges)
end = time()
print("\n--- Hierarchical clustering ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
display(nodes, edges, out)


start = time()
out, mod = girvan_newman(nodes, edges)
end = time()
print("\n--- Girvan-Newman ---")
print("modularity: ", round(mod, 2))
print("time: ", round(end - start, 2))
display(nodes, edges, out)





