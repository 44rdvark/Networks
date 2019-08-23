from networkx import read_gml
from networks.clauset_newman_moore import clauset_newman_moore
from networks.common.display import display
from networks.common.evaluate_similarity import evaluate
from networks.common.modularity import get_modularity
from networks.common.partition_to_communities import get_partitioning
from networks.girvan_newman import girvan_newman
from networks.girvan_newman_foresight import girvan_newman_foresight
from networks.hierarchical_clustering import hierarchical_clustering
from networks.blondel import blondel
from time import time

from networks.hierarchical_clustering_foresight import hierarchical_clustering_foresight


def upn(nodes):
    n = []
    for i in range(len(nodes)):
        n.append(nodes[i] + 1)
    return n


def upe(edges):
    e = []
    for edge in edges:
        e.append((edge[0] + 1, edge[1] + 1))
    return e


def upc(coms):
    for i in range(len(coms)):
        for j in range(len(coms[i])):
            coms[i][j] = coms[i][j] + 1

g = read_gml('../data/karate.gml', label='id')
nodes = list(g.nodes())
edges = list(g.edges())
for i in range(len(nodes)):
    nodes[i] = nodes[i] - 1
for i in range(len(edges)):
    edges[i] = (edges[i][0] - 1, edges[i][1] - 1)
proper = ((0, 1, 2, 3, 7, 13, 19, 17, 21, 11,  10, 12, 4, 5, 6, 16),
               (8, 30, 9, 33, 22, 14, 26, 15, 29, 20, 32, 18, 23, 28, 27, 31, 25, 24))
start = time()
out, mod = blondel(nodes, edges)
end = time()
print("--- Blondel ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
print(round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))
n = upn(nodes)
e = upe(edges)
display(n, e, out)


start = time()
out, mod = clauset_newman_moore(nodes, edges)
end = time()
print("\n--- Clauset-Newman-Moore ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print(round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))
n = upn(nodes)
e = upe(edges)
display(n, e, out)


start = time()
out, mod = hierarchical_clustering(nodes, edges)
end = time()
print("\n--- Hierarchical clustering ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print(round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))
n = upn(nodes)
e = upe(edges)
display(n, e, out)

start = time()
out, mod = hierarchical_clustering_foresight(nodes, edges, 2)
end = time()
print("\n--- Hierarchical clustering foresight ---")
print("modularity:", round(mod, 2))
print("time", round(end - start, 2))
print(round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))
n = upn(nodes)
e = upe(edges)
display(n, e, out)

start = time()
out, mod = girvan_newman(nodes, edges)
end = time()
print("\n--- Girvan-Newman ---")
print("modularity: ", round(mod, 2))
print("time: ", round(end - start, 2))
print(round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))
n = upn(nodes)
e = upe(edges)
display(n, e, out)

start = time()
out, mod = girvan_newman_foresight(nodes, edges, 2)
end = time()
print("\n--- Girvan-Newman foresight---")
print("modularity: ", round(mod, 2))
print("time: ", round(end - start, 2))
print(round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))
n = upn(nodes)
e = upe(edges)
display(n, e, out)

print("\n--- Proper ---")

print("modularity: ", round(get_modularity(nodes, edges, get_partitioning(proper)), 2))
print(round(evaluate(get_partitioning(proper), get_partitioning(proper)), 2))

display(n, e, proper)


