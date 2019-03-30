def evaluate(actual, found):
    n_nodes = len(actual)
    dist = 0
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if (found[i] == found[j]) != (actual[i] == actual[j]):
                dist += 1
    return dist
