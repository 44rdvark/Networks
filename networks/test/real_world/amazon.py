from networks.algorithms.clauset_newman_moore import clauset_newman_moore
from networks.algorithms.girvan_newman import girvan_newman
from networks.algorithms.hierarchical_clustering import hierarchical_clustering
from networks.algorithms.blondel import blondel
from time import time

#  The network was studied by Leskovec and Yang - refer to:
#  Yang, J. and Leskovec, J. (2012). Defining and evaluating network communities
#  based on ground-truth. In 2012 IEEE 12th International Conference on Data Mining,
#  pages 745–754.
#  The vertices denote products sold on Amazon website, while an edge between two nodes
#  exists if the two products were frequently purchased together.
#  The network consists of 334863 nodes and 925872 edges.


f = open("data/amazon.txt", "r")
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
