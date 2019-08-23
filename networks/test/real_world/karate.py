from networkx import read_gml
from networks.algorithms.clauset_newman_moore import clauset_newman_moore
from networks.common.display import display
from networks.common.evaluate_similarity import evaluate
from networks.common.modularity import get_modularity
from networks.common.partition_to_communities import get_partitioning
from networks.algorithms.girvan_newman import girvan_newman
from networks.algorithms.hierarchical_clustering import hierarchical_clustering
from networks.algorithms.blondel import blondel
from time import time


#  The analyzed network is one of a university karate club studied by Zachary - refer to:
#  Zachary, W. (1976). An information flow model for conflict and fission in small
#  groups. Journal of anthropological research, 33.
#  The 34 nodes of the network correspond to members  of the club, while the 78 edges each
#  represent an interaction between two members that took place outside of the club.
#  At some stage, while the network was studied, a conflict between members labeled as 1 and 34
#  led to a division of the group into two separate clubs.


def refactor_dataset(nodes, edges):
    n = []
    for i in range(len(nodes)):
        n.append(nodes[i] + 1)
    e = []
    for edge in edges:
        e.append((edge[0] + 1, edge[1] + 1))
    return n, e


g = read_gml('data/karate.gml', label='id')
nodes = list(g.nodes())
edges = list(g.edges())
for i in range(len(nodes)):
    nodes[i] = nodes[i] - 1
for i in range(len(edges)):
    edges[i] = (edges[i][0] - 1, edges[i][1] - 1)
n, e = refactor_dataset(nodes, edges)
proper = ((0, 1, 2, 3, 7, 13, 19, 17, 21, 11,  10, 12, 4, 5, 6, 16),
               (8, 30, 9, 33, 22, 14, 26, 15, 29, 20, 32, 18, 23, 28, 27, 31, 25, 24))
start = time()
out, mod = blondel(nodes, edges)
end = time()
print("--- Blondel ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))
display(n, e, out)


start = time()
out, mod = clauset_newman_moore(nodes, edges)
end = time()
print("\n--- Clauset-Newman-Moore ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))
display(n, e, out)


start = time()
out, mod = hierarchical_clustering(nodes, edges)
end = time()
print("\n--- Hierarchical clustering ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))
display(n, e, out)

start = time()
out, mod = girvan_newman(nodes, edges)
end = time()
print("\n--- Girvan-Newman ---")
print("modularity:", round(mod, 2))
print("time:", round(end - start, 2))
print("Rand index:", round(evaluate(get_partitioning(out), get_partitioning(proper)), 2))
display(n, e, out)

print("\n--- Proper ---")

print("modularity:", round(get_modularity(nodes, edges, get_partitioning(proper)), 2))

display(n, e, proper)


