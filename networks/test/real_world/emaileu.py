from networks.algorithms.clauset_newman_moore import clauset_newman_moore
from networks.common.evaluate_similarity import evaluate
from networks.common.modularity import get_modularity
from networks.common.partition_to_communities import get_partitioning
from networks.algorithms.girvan_newman import girvan_newman
from networks.algorithms.hierarchical_clustering import hierarchical_clustering
from networks.algorithms.blondel import blondel
from time import time

#  Compiled by Leskovec et al. - refer to:
#  Yin, H., Benson, A. R., Leskovec, J., and Gleich, D. F. (2017). Local higher-order
#  graph clustering. KDD : proceedings. International Conference on Knowledge Discovery
#  and Data Mining, 2017:555–564.
#  This dataset represents anonymized data about email correspondence between members
#  of a certain European research institution. Each directed edge in the network corresponds
#  to an email sent between a pair of members represented by nodes.
#  I have removed self-loops and edge direction from the graph to make it suitable for testing.
#  The modified graph contains 1005 nodes, 16064 edges and 42 ground truth communities,
#  each corresponding to a department within the research institution,with a node contained
#  in a community if the member represented by it belonged to the respective department.


f = open("data/email.txt", "r")
f_com = open("data/email_communities.txt", "r")
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


nodes = [i for i in range(1005)]

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
print("time: ", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))

print("\n--- Proper ---")

print("modularity: ", round(get_modularity(nodes, edges, get_partitioning(proper)), 2))
print(round(evaluate(get_partitioning(proper), get_partitioning(proper)), 2))


