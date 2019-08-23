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

f = open("../data/email.txt", "r")
f_com = open("../data/email_communities.txt", "r")
edges = []
proper = [[] for _ in range(42)]
d = {}
for line in f.readlines():
    e = line.split(" ")
    a = int(e[0])
    b = int(e[1])
    if a != b and d.get((max(a, b), min(a, b))) is None:
        edges.append((a, b))
        d[(max(a, b), min(a, b))] = 0
for line in f_com.readlines():
    p = line.split(" ")
    proper[int(p[1])].append(int(p[0]))

print(len(edges))

nodes = [i for i in range(1005)]

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


