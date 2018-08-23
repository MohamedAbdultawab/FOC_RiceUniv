"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
from clustering import hierarchical_clustering as h_clustering
from clustering import kmeans_clustering as k_clustering
import alg_clusters_matplotlib
import matplotlib.pyplot as plt
import cluster as alg_cluster
from matplotlib.ticker import FuncFormatter


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "/media/toba/FOCUS/2_Fundamentals of Computing Rice University/algorithmic-thinking-2/02_module-3-project-and-application/02_application-3-comparison-of-clustering-algorithms/"
DATA_3108_URL = DIRECTORY + "unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = open(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print("Loaded", len(data_lines), "data points")
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0],
             float(tokens[1]),
             float(tokens[2]),
             int(tokens[3]),
             float(tokens[4])]
            for tokens in data_tokens]


###################################################
# Code to load data tables


def compute_distortion(cluster_list, data_table):
    return sum(cluster.cluster_error(data_table) for cluster in cluster_list)


#####################################################################
# Code to load cancer data, compute a clustering and
# visualize the results


def run_example():
    """
    Load a data table, compute a list of clusters and
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """

    # Code to load data

    data_table = load_data_table(DATA_111_URL)

    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]),
                                                  line[1],
                                                  line[2],
                                                  line[3],
                                                  line[4]))

    # Code to make the cluster lists, their clustering
    # and visualization

    cluster_list = h_clustering(singleton_list, 9)
    print("Displaying", len(cluster_list), "hierarchical clusters")

    cluster_list = k_clustering(singleton_list, 9, 5)
    print("Displaying", len(cluster_list), "k-means clusters")

    # draw the clusters using matplotlib

    # alg_clusters_matplotlib.plot_clusters(data_table,
    #                                       cluster_list,
    #                                       False)
    alg_clusters_matplotlib.plot_clusters(data_table,
                                          cluster_list,
                                          True)  # add cluster centers

    # Computing clusters distortion
    print(compute_distortion(cluster_list, data_table))


def Q10():

    def copy_clusters(cluster_list):
        return list(cluster.copy()for cluster in cluster_list)

    # Code to load data

    data_table_111 = load_data_table(DATA_111_URL)

    list_111 = []
    for line in data_table_111:
        list_111.append(alg_cluster.Cluster(set([line[0]]),
                                            line[1],
                                            line[2],
                                            line[3],
                                            line[4]))
    data_set_111_h = [h_clustering(copy_clusters(list_111), num_clusters)
                      for num_clusters in range(6, 21)]

    distortion_111_h = [compute_distortion(cluster_list, data_table_111)
                        for cluster_list in data_set_111_h]

    data_set_111_k = [k_clustering(copy_clusters(list_111), num_clusters, 5)
                      for num_clusters in range(6, 21)]

    distortion_111_k = [compute_distortion(cluster_list, data_table_111)
                        for cluster_list in data_set_111_k]

    data_table_290 = load_data_table(DATA_290_URL)

    list_290 = []
    for line in data_table_290:
        list_290.append(alg_cluster.Cluster(set([line[0]]),
                                            line[1],
                                            line[2],
                                            line[3],
                                            line[4]))
    data_set_290_h = [h_clustering(copy_clusters(list_290), num_clusters)
                      for num_clusters in range(6, 21)]

    distortion_290_h = [compute_distortion(cluster_list, data_table_290)
                        for cluster_list in data_set_290_h]

    data_set_290_k = [k_clustering(copy_clusters(list_290), num_clusters, 5)
                      for num_clusters in range(6, 21)]

    distortion_290_k = [compute_distortion(cluster_list, data_table_290)
                        for cluster_list in data_set_290_k]

    data_table_896 = load_data_table(DATA_896_URL)

    list_896 = []
    for line in data_table_896:
        list_896.append(alg_cluster.Cluster(set([line[0]]),
                                            line[1],
                                            line[2],
                                            line[3],
                                            line[4]))

    data_set_896_h = [h_clustering(copy_clusters(list_896), num_clusters)
                      for num_clusters in range(6, 21)]

    distortion_896_h = [compute_distortion(cluster_list, data_table_896)
                        for cluster_list in data_set_896_h]

    data_set_896_k = [k_clustering(copy_clusters(list_896), num_clusters, 5)
                      for num_clusters in range(6, 21)]

    distortion_896_k = [compute_distortion(cluster_list, data_table_896)
                        for cluster_list in data_set_896_k]

    x_data = [num for num in range(6, 21)]

    plt.style.use('ggplot')

    def expo(x, pos):
        """The two args are the value and tick position"""
        return str(x / (10**11))

    formatter = FuncFormatter(expo)

    fig0, ax0 = plt.subplots(num='Hierarchical & k-means clustering - 111 county')
    ax0.plot(x_data, distortion_111_h, color='g', label='Hierarchical')
    ax0.plot(x_data, distortion_111_k, color='b', label='K-means')
    ax0.set(title='Distortion of the clusterings produced by Hierarchical\nand K-means - 111 county',
            xlabel='Number of clusters',
            ylabel='Distortion * 10 ^ 11')
    ax0.legend(loc='best')
    ax0.yaxis.set_major_formatter(formatter)
    fig0.savefig('data_111_distortion.png',
                 dpi=300,
                 format='png',
                 transparent=False,
                 orientation='landscape',
                 bbox_inches='tight',
                 pad_inches=0.3)

    fig1, ax1 = plt.subplots(num='Hierarchical & k-means clustering - 290 county')
    ax1.plot(x_data, distortion_290_h, color='g', label='Hierarchical')
    ax1.plot(x_data, distortion_290_k, color='b', label='K-means')
    ax1.set(title='Distortion of the clusterings produced by Hierarchical\nand K-means - 290 county',
            xlabel='Number of clusters',
            ylabel='Distortion * 10 ^ 11')
    ax1.legend(loc='best')
    ax1.yaxis.set_major_formatter(formatter)
    fig1.savefig('data_290_distortion.png',
                 dpi=300,
                 format='png',
                 transparent=False,
                 orientation='landscape',
                 bbox_inches='tight',
                 pad_inches=0.3)

    fig2, ax2 = plt.subplots(num='Hierarchical & k-means clustering - 896 county')
    ax2.plot(x_data, distortion_896_h, color='g', label='Hierarchical')
    ax2.plot(x_data, distortion_896_k, color='b', label='K-means')
    ax2.set(title='Distortion of the clusterings produced by Hierarchical\nand K-means - 896 county',
            xlabel='Number of clusters',
            ylabel='Distortion * 10 ^ 11')
    ax2.legend(loc='best')
    ax2.yaxis.set_major_formatter(formatter)
    fig2.savefig('data_896_distortion.png',
                 dpi=300,
                 format='png',
                 transparent=False,
                 orientation='landscape',
                 bbox_inches='tight',
                 pad_inches=0.3)

    # plt.show()


Q10()
