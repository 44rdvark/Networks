from networkx import read_gml
from networks.clauset_newman_moore import clauset_newman_moore
from networks.common.display import display
from networks.common.evaluate_similarity import evaluate
from networks.common.partition_to_communities import get_partitioning
from networks.girvan_newman import girvan_newman
from networks.hierarchical_clustering import hierarchical_clustering
from networks.blondel import blondel
from time import time

f = open("/home/adam/PycharmProjects/Networks/networks/data/amazon.txt", "r")
edges = []
m = 0
d = {}
for line in f.readlines():
    e = line.split("\t")
    a = d.get(int(e[0]))
    b = d.get(int(e[1]))
    if a is None:
        a = m
        d[int(e[0])] = m
        m += 1
    if b is None:
        b = m
        d[(int(e[1]))] = m
        m += 1
    edges.append((a, b))

nodes = [i for i in range(m)]

'''start = time()
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
'''
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
