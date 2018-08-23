"""
Analysis of the performance of two clustering methods
on various subsetsof our county-level cancer risk data set.
    In particular, we will compare these two clustering methods in three areas:
           * Efficiency - Which method computes clusterings more efficiently?
           * Automation - Which method requires less human supervision
             to generate reasonable clusterings?
           * Quality - Which method generates clusterings with less error?"""

from timeit import timeit
import matplotlib.pyplot as plt

setup = """from random import random, uniform
from cluster import Cluster
from closest_pair_and_clustering import fast_closest_pair, slow_closest_pair


def gen_random_clusters(num_clusters):
    for dummy_i in range(num_clusters):
        yield Cluster(set(), uniform(-1.0, 1.0), uniform(-1.0, 1.0), 0, 0)


cluster_lists = [list(gen_random_clusters(num_clusters)) for num_clusters in range(2, 201)]"""

code_for_fast = """fast_closest_pair(cluster_lists[{}])"""

times_for_fast = [timeit(stmt=code_for_fast.format(idx),
                  setup=setup,
                  number=50) for idx in range(199)]

code_for_slow = """slow_closest_pair(cluster_lists[{}])"""

times_for_slow = [timeit(stmt=code_for_slow.format(idx),
                  setup=setup,
                  number=50) for idx in range(199)]

plt.plot(times_for_fast, color='g', label='Fast Method')
plt.plot(times_for_slow, color='b', label='Slow Method')

plt.title('Slow and fast Closest pair - Desktop', fontsize=18, color='#ff8800')

plt.xlabel('Number of clusters', fontsize=14, color='#ff8800')

plt.ylabel('Time in seconds', fontsize=14, color='#ff8800')

plt.legend(loc='best', labels=['Fast Method', 'Slow Method'])

plt.show()
# plt.savefig('Q1', dpi=300, format='png', transparent=False, orientation='landscape', bbox_inches='tight', pad_inches=0.3)
