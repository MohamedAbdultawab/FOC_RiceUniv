"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""
from cluster import Cluster
import math


######################################################
# Code for closest pairs of clusters


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters

    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]),
            min(idx1, idx2),
            max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters

    Output: tuple of the form (dist, idx1, idx2) where the main_clusters of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    output = (float('inf'), -1, -1)
    for idx1 in range(len(cluster_list)):
        for idx2 in range(len(cluster_list)):
            if idx1 != idx2:
                output = min(output, pair_distance(cluster_list, idx1, idx2))

    return output


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    main_clusters are in ascending order

    Output: tuple of the form (dist, idx1, idx2) where the main_clusters of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    cluster_list.sort(key=lambda cluster: cluster.horiz_center())
    cluster_list_len = len(cluster_list)
    if cluster_list_len <= 3:
        output = slow_closest_pair(cluster_list)

    else:
        half_cluster_list_len = cluster_list_len // 2
        left_cluster_list = cluster_list[:half_cluster_list_len]

        right_cluster_list = cluster_list[half_cluster_list_len:]

        left_output = fast_closest_pair(left_cluster_list)
        right_output = fast_closest_pair(right_cluster_list)

        # adjusting the indices of the right half, so it consist with the whole list
        right_output = (right_output[0],
                        right_output[1] + half_cluster_list_len,
                        right_output[2] + half_cluster_list_len)

        output = min(left_output, right_output)
        mid = 0.5 * (cluster_list[half_cluster_list_len - 1].horiz_center() +
                     cluster_list[half_cluster_list_len].horiz_center())
        output = min(output, closest_pair_strip(cluster_list, mid, output[0]))

    return output


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip

    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the main_clusters of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    clusters_within_width = [cluster_list.index(cluster)
                             for cluster in cluster_list
                             if abs(cluster.horiz_center() -
                                    horiz_center) < half_width]

    clusters_within_width.sort(key=lambda idx: cluster_list[idx].vert_center())
    within_width_len = len(clusters_within_width)
    output = (float('inf'), -1, -1)

    for idx_i in range(within_width_len - 1):

        for idx_j in range(idx_i + 1,
                           min(idx_i + 3, within_width_len - 1) + 1):
            output = min(output, pair_distance(cluster_list,
                                               clusters_within_width[idx_i],
                                               clusters_within_width[idx_j]))

    return output

######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list

    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        output = fast_closest_pair(cluster_list)
        cluster1_idx, cluster2_idx = output[1], output[2]
        cluster_list[cluster1_idx].merge_clusters(cluster_list[cluster2_idx])
        del cluster_list[cluster2_idx]

    return cluster_list


######################################################################
# Code for k-means clustering


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list

    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    cluster_list = sorted(cluster_list,
                          key=lambda cluster: cluster.total_population(),
                          reverse=True)

    main_clusters = cluster_list[:num_clusters]

    for dummy_i in range(num_iterations):
        clusters = [Cluster(set([]),
                            0,
                            0,
                            0,
                            0)
                    for dummy_x in range(num_clusters)]

        for cluster_idx in range(len(cluster_list)):
            distance_lst = [(cluster_list[cluster_idx].distance(cluster), idx)
                            for idx, cluster in enumerate(main_clusters)]

            least_distance = min(distance_lst)[1]
            clusters[least_distance].merge_clusters(cluster_list[cluster_idx])

        main_clusters = clusters[:]

    return main_clusters


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering

    Note that method may return num_clusters or num_clusters + 1 final clusters
    """

    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters) / num_clusters

    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)

    return cluster_list
