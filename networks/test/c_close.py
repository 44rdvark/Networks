from random import shuffle, uniform
from networks.clauset_newman_moore import clauset_newman_moore
from networks.common.c_close import c_close
from networks.common.modularity import get_modularity
from networks.girvan_newman import girvan_newman
from networks.hierarchical_clustering import hierarchical_clustering
from networks.blondel import blondel
from time import time


# initializes random network with equally sized communities
# returns nodes and edges of generated network and expected partitioning
def generate_random_network(n_communities, community_size, prob_inner, prob_outer):
    n_nodes = n_communities * community_size
    nodes = list(range(n_nodes))
    edges = []
    partitioning = list(range(n_communities)) * community_size
    shuffle(partitioning)
    for i in range(0, n_nodes):
        for j in range(i + 1, n_nodes):
            rand = uniform(0, 1)
            if partitioning[i] == partitioning[j] and rand <= prob_inner \
                    or partitioning[i] != partitioning[j] and rand <= prob_outer:
                edges.append((i, j))
    return nodes, edges, partitioning


nodes, edges, partitioning = generate_random_network(10, 10, 0.8, 0.2)

c = 5
new_edges = c_close(nodes, edges, c)
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

print("\n\n---", c, "Closed ---\n\n")

start = time()
out, mod = blondel(nodes, new_edges)
end = time()
print("--- Blondel ---")
print("modularity:", round(get_modularity(nodes, edges, out), 2))
print("time:", round(end - start, 2))

start = time()
out, mod = clauset_newman_moore(nodes, new_edges)
end = time()
print("\n--- Clauset-Newman-Moore ---")
print("modularity:", round(get_modularity(nodes, edges, out), 2))
print("time", round(end - start, 2))

start = time()
out, mod = hierarchical_clustering(nodes, new_edges)
end = time()
print("\n--- Hierarchical clustering ---")
print("modularity:", round(get_modularity(nodes, edges, out), 2))
print("time", round(end - start, 2))

start = time()
out, mod = girvan_newman(nodes, new_edges)
end = time()
print("\n--- Girvan-Newman ---")
print("modularity:", round(get_modularity(nodes, edges, out), 2))
print("time: ", round(end - start, 2))