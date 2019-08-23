from time import time
from networks.clauset_newman_moore import clauset_newman_moore
from networks.common.modularity import get_modularity
from networks.common.partition_to_communities import get_partitioning
from networks.common.random_network import generate_synthetic_network
from networks.girvan_newman import girvan_newman
from networks.hierarchical_clustering import hierarchical_clustering
from networks.blondel import blondel
from networks.common.evaluate_similarity import evaluate
import matplotlib.pyplot as plt
c = 10
k = 12
p_in = 1
p_out = 1./k
rp = 1
dp = 17
x = [0] * dp
yt_blo = [0] * dp
yt_cnm = [0] * dp
yt_gn = [0] * dp
yt_hc = [0] * dp

ys_blo = [0] * dp
ys_cnm = [0] * dp
ys_gn = [0] * dp
ys_hc = [0] * dp

ym_blo = [0] * dp
ym_cnm = [0] * dp
ym_gn = [0] * dp
ym_hc = [0] * dp
ym_pro = [0] * dp
t = 1
for j in range(t):
    p_in = 1
    p_out = 1. / k
    for i in range(dp):

        nodes, edges, partitioning = generate_synthetic_network(c, k, p_in, p_out)
        print(len(nodes), len(edges))
        start = time()
        out, mod = blondel(nodes, edges)
        end = time()
        s = evaluate(get_partitioning(out), partitioning)
        x[i] = p_in
        yt_blo[i] += end-start
        ym_blo[i] += mod
        ys_blo[i] += s

        start = time()
        out, mod = clauset_newman_moore(nodes, edges)
        end = time()
        s = evaluate(get_partitioning(out), partitioning)
        yt_cnm[i] += end-start
        ym_cnm[i] += mod
        ys_cnm[i] += s

        start = time()
        out, mod = hierarchical_clustering(nodes, edges)
        end = time()
        s = evaluate(get_partitioning(out), partitioning)
        yt_hc[i] += end - start
        ym_hc[i] += mod
        ys_hc[i] += s

        start = time()
        out, mod = girvan_newman(nodes, edges)
        end = time()
        s = evaluate(get_partitioning(out), partitioning)
        yt_gn[i] += end - start
        ym_gn[i] += mod
        ys_gn[i] += s

        ym_pro[i] += get_modularity(nodes, edges, partitioning)

        p_in -= 0.05
        p_out += 0.05 / c

for i in range(dp):
    yt_blo[i] /= float(t)
    yt_cnm[i] /= float(t)
    yt_gn[i] /= float(t)
    yt_hc[i] /= float(t)

    ys_blo[i] /= float(t)
    ys_cnm[i] /= float(t)
    ys_gn[i] /= float(t)
    ys_hc[i] /= float(t)

    ym_blo[i] /= float(t)
    ym_cnm[i] /= float(t)
    ym_gn[i] /= float(t)
    ym_hc[i] /= float(t)
    ym_pro[i] /= float(t)

plt.plot(x, yt_blo, '--ob', label="Blo")
plt.plot(x, yt_cnm, '--og', label="CNM")
plt.plot(x, yt_gn, '--or', label="GN")
plt.plot(x, yt_hc, '--oy', label="Hc")
plt.legend()
plt.axis([1/6, 1, -1, 40])
plt.xlabel(r'$p_{in} = \frac{22}{12} - 10p_{out}$')
plt.ylabel('Time (seconds)')
plt.show()

plt.plot(x, ys_blo, '--ob', label="Blo")
plt.plot(x, ys_cnm, '--og', label="CNM")
plt.plot(x, ys_gn, '--or', label="GN")
plt.plot(x, ys_hc, '--oy', label="Hc")
plt.legend()
plt.axis([1/6, 1, 0.4, 1.1])
plt.xlabel(r'$p_{in} = \frac{22}{12} - 10p_{out}$')
plt.ylabel('Similarity')
plt.show()

plt.plot(x, ym_blo, '--ob', label="Blo")
plt.plot(x, ym_cnm, '--og', label="CNM")
plt.plot(x, ym_gn, '--or', label="GN")
plt.plot(x, ym_hc, '--oy', label="Hc")
plt.plot(x, ym_pro, '--ok', label="Act")

plt.legend()
plt.axis([1/6, 1, -0.1, 0.5])
plt.xlabel(r'$p_{in} = \frac{22}{12} - 10p_{out}$')
plt.ylabel('Modularity')
plt.show()

