"""
Project #1
Function to make digraphs
Two short functions to compute the distribution
of the in-degrees for nodes in these graphs
"""
from collections import Counter
# from matplotlib import pyplot as plt


# class Graph(object):
#     """docstring for Graph"""
#     def __init__(self, nodes=[], edges=[], directed=False):
#         self._graph = dict()
#         self._deg_dist = {}  # Degree Distribution
#         if len(nodes):
#             self.make_graph(nodes, edges, directed)

#     def make_complete(self, num_nodes, directed=False):
#         nodes = list(range(num_nodes))
#         edges = [(node_1, node_2) for node_1 in nodes for node_2 in nodes if node_1 != node_2]
#         self.make_graph(nodes, edges, directed)

#     def make_graph(self, nodes, edges, directed=False):
#         for node in nodes:
#             self._graph[node] = set()

#         if not directed:
#             edges = set([sorted(edge) for edge in edges])

#         for edge in edges:
#             self._graph[edge[0]].add(edge[1])

#     def in_degrees(self):
#         """
#         Returns a dictionary of in-degrees of the nodes
#         of the input digraph
#         """
#         degrees = dict.fromkeys(self._graph, 0)
#         edges = []
#         for value in self._graph.values():
#             edges += list(value)
#         for edge in edges:
#             degrees[edge] += 1
#         return degrees

#     def in_degree_distribution(self, normalized=False):
#         """Returns the degree distribution of a digraph"""
#         num_nodes = float(len(self._graph))
#         degrees = self.in_degrees(self._graph)
#         self._deg_dist = dict(Counter(degrees.values()))
#         if normalized:
#             for degree in iter(self._deg_dist):
#                 self._deg_dist[degree] /= num_nodes
#         return self._deg_dist

#     def plot(self, log=True, file_name='', title='', xlabel='', ylabel='', color='#634017'):
#         if log:
#             plt.loglog(self._graph.keys(), self._graph.values(), 'o', color=color)
#         else:
#             plt.plot(self._graph.keys(), self._graph.values(), 'o', color=color)

#         plt.title(title, fontsize=18, color='#ff8800')
#         plt.xlabel(xlabel, fontsize=14, color='#ff8800')
#         plt.ylabel(ylabel, fontsize=14, color='#ff8800')
#         if file_name:
#             plt.savefig(file_name, dpi=300, format='png', transparent=False, orientation='landscape', bbox_inches='tight', pad_inches=0.3)


def make_digraph(nodes, edges):
    """Returns a digraph from a list of nodes
    and a list of edges represented as tuples"""
    graph = dict()
    for node in nodes:
        graph[node] = set()
    for edge in edges:
        graph[edge[0]].add(edge[1])
    return graph


VERTICES_0 = [0, 1, 2]
EDGES_0 = [(0, 1), (0, 2)]
EX_GRAPH0 = make_digraph(VERTICES_0, EDGES_0)

VERTICES_1 = [0, 1, 2, 3, 4, 5, 6]
EDGES_1 = [(0, 1), (0, 4), (0, 5),
           (1, 2), (1, 6), (2, 3),
           (3, 0), (4, 1), (5, 2)]
EX_GRAPH1 = make_digraph(VERTICES_1, EDGES_1)

VERTICES_2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
EDGES_2 = [(0, 1), (0, 4), (0, 5),
           (1, 2), (1, 6), (2, 3),
           (2, 7), (3, 7), (4, 1),
           (5, 2), (7, 3), (8, 1),
           (8, 2), (9, 0), (9, 3),
           (9, 4), (9, 5), (9, 6),
           (9, 7)]
EX_GRAPH2 = make_digraph(VERTICES_2, EDGES_2)


def make_complete_graph(num_nodes):
    """Returns a complete graph"""
    nodes = list(range(num_nodes))
    edges = [(node_1, node_2) for node_1 in nodes for node_2 in nodes if node_1 != node_2]
    return make_digraph(nodes, edges)


def compute_in_degrees(digraph):
    """Returns a dictionary of in-degrees of the nodes
    of the input digraph"""
    degrees = dict.fromkeys(digraph, 0)
    edges = []
    for value in digraph.values():
        edges += list(value)
    for edge in edges:
        degrees[edge] += 1
    return degrees


def in_degree_distribution(digraph):
    """Returns the degree distribution of a digraph"""
    degrees = compute_in_degrees(digraph)
    return dict(Counter(degrees.values()))
