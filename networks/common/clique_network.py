def generate_clique_network(clique_size, n_cliques):
    vertices = []
    edges = []
    partitioning = [0] * clique_size * n_cliques
    for i in range(n_cliques):
        for j in range(clique_size):
            partitioning[i * clique_size + j] = i
    for i in range(n_cliques):
        for j in range(clique_size):
            vertices.append(i * clique_size + j)
            for k in range (j + 1, clique_size):
                edges.append((i * clique_size + j, (i * clique_size + k)))
        edges.append((i * clique_size, (i * clique_size + clique_size * n_cliques - 1) % (clique_size * n_cliques)))

    return vertices, edges, partitioning

