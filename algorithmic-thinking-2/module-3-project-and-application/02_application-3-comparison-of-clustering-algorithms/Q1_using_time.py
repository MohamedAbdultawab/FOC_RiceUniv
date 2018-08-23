"""
analysis of the performance of two clustering methods on various subsets
of our county-level cancer risk data set.
    In particular, we will compare these two clustering methods in three areas:

        Efficiency - Which method computes clusterings more efficiently?

        Automation - Which method requires less human supervision to generate
        reasonable clusterings?

        Quality - Which method generates clusterings with less error?
"""
import matplotlib.pyplot as plt
from random import uniform
from cluster import Cluster
from time import time
from closest_pair_and_clustering import fast_closest_pair, slow_closest_pair


def timeit(func, *args, **kwargs):
    start = time()
    func(*args, **kwargs)
    return time() - start


def gen_random_clusters(num_clusters):

    for dummy_i in range(num_clusters):
        yield Cluster(set(), uniform(-1.0, 1.0), uniform(-1.0, 1.0), 0, 0)


cluster_lists = [list(gen_random_clusters(num_clusters))
                 for num_clusters in range(2, 201)]


times_for_fast = [timeit(fast_closest_pair, cluster_list)
                  for cluster_list in cluster_lists]

times_for_slow = [timeit(slow_closest_pair, cluster_list)
                  for cluster_list in cluster_lists]

# Plotting
plt.plot(times_for_fast, color='g', label='Fast Method')
plt.plot(times_for_slow, color='b', label='Slow Method')

plt.title('Slow and fast Closest pair - Desktop',
          fontsize=18,
          color='#ff8800')
plt.xlabel('Number of clusters',
           fontsize=14,
           color='#ff8800')
plt.ylabel('Time in seconds',
           fontsize=14,
           color='#ff8800')
plt.legend(loc='best', labels=['Fast Method',
                               'Slow Method'])
plt.show()
# plt.savefig('Q3', dpi=300, format='png', transparent=False, orientation='landscape', bbox_inches='tight', pad_inches=0.3)
