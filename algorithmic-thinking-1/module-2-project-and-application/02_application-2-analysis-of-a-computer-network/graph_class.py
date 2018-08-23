#!/usr/bin python3.5
import random
from itertools import chain
from collections import deque, Counter
from matplotlib import pyplot as plt
from copy import deepcopy


class Queue(object):
    """
    Queue wrapper implementation of deque
    """
    def __init__(self, arg=list()):
        self._queue = deque(arg)

    def __iter__(self):  # TODO: find a way to do it without using sorted
        for value in sorted(self._queue, reverse=False):
            yield value

    def __len__(self):
        return len(self._queue)

    def __str__(self):
        return str(self._queue)

    def enqueue(self, value):
        """
        docstring for enqueue
        """
        self._queue.appendleft(value)

    def dequeue(self):
        """
        docstring for dequeue
        """
        return self._queue.pop()

    def is_empty(self):
        """
        Return True when the queue is empty
        False otherwise
        """
        return True if len(self._queue) == 0 else False

    def clear(self):
        """
        Clear out the queue
        """
        self._queue.clear()


class Graph(object):
    """docstring for Graph"""
    def __init__(self, nodes=[], edges=[], directed=False):
        self._graph = dict()
        self._deg_dist = {}  # Degree Distribution
        if len(nodes):
            self._make_graph(nodes, edges, directed)

    def make_complete(self, num_nodes, directed=False):
        nodes = list(range(num_nodes))
        edges = [(node_1, node_2) for node_1 in nodes for node_2 in nodes if node_1 != node_2]
        self._make_graph(nodes, edges, directed)

    def _make_graph(self, nodes, edges, directed=False):
        for node in nodes:
            self._graph[node] = set()

        if len(edges) == 0:
            return

        if not directed:
            edges = set([tuple(sorted(edge)) for edge in edges])

        for edge in edges:
            self._graph[edge[0]].add(edge[1])

    def __len__(self):
        return len(self._graph)

    def __contains__(self, value):
        return value in self._graph

    def __setitem__(self, node, edges):
        assert not (edges is set and node is int)
        self._graph[node] = edges

    def __getitem__(self, node):
        assert not (node is int)
        return self._graph[node]

    def __delitem__(self, node):
        del self._graph[node]
        for key, edges in self._graph.items():
            if node in edges:
                self._graph[key].remove(node)

    def get_nodes(self):
        return self._graph.keys()

    def get_num_edges(self):
        return sum([len(x) for x in self._graph.values()])

    def copy(self):
        return deepcopy(self._graph)

    def in_degrees(self):
        """
        Returns a dictionary of in-degrees of the nodes
        of the input digraph
        """
        degrees = dict.fromkeys(self._graph, 0)
        edges = []
        for value in self._graph.values():
            edges += list(value)
        for edge in edges:
            degrees[edge] += 1
        return degrees

    def out_degrees(self):
        """Returns a dictionary of out-degrees of the nodes
        of the input digraph"""
        degrees = dict()
        for node in self._graph:
            degrees[node] = len(self._graph[node])
        return degrees

    def in_degree_distribution(self, normalized=False):
        """Returns the degree distribution of a digraph"""
        num_nodes = float(len(self))
        degrees = self.in_degrees()
        self._deg_dist = dict(Counter(degrees.values()))
        if normalized:
            for degree in iter(self._deg_dist):
                self._deg_dist[degree] /= num_nodes
        return self._deg_dist

    def plot(self, log=True, file_name='', title='', xlabel='', ylabel='', color='#634017'):
        if log:
            plt.loglog(self._graph.keys(), self._graph.values(), 'o', color=color)
        else:
            plt.plot(self._graph.keys(), self._graph.values(), 'o', color=color)

        plt.title(title, fontsize=18, color='#ff8800')
        plt.xlabel(xlabel, fontsize=14, color='#ff8800')
        plt.ylabel(ylabel, fontsize=14, color='#ff8800')
        if file_name:
            plt.savefig(file_name, dpi=300, format='png', transparent=False, orientation='landscape', bbox_inches='tight', pad_inches=0.3)


class ER(Graph):

    def __init__(self, num_nodes, probability, directed=False):
        nodes = range(num_nodes)
        edges = list(chain.from_iterable([(i, j), (j, i)]
                     for i in nodes
                     for j in nodes
                     if i != j and random.random() < probability))

        super().__init__(nodes, edges, directed)


class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm

    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]

    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that each node number
        appears in correct ratio

        Returns:
        Set of nodes
        """

        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        # update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors


def load_graph_data(file_name):
    """
    Function that loads a graph given a text
    representation of the graph

    Returns a dictionary that models a graph
    """
    graph_file = open(file_name)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_file.close()
    graph_lines = graph_lines[:-1]

    print("Loaded graph with", len(graph_lines), "nodes")

    nodes = []
    edges = []
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        nodes.append(node)
        for neighbor in neighbors[1:-1]:
            edges.append((node, int(neighbor)))
    return nodes, edges


def bfs_visited(ugraph, start_node):
    """
    Breadth-first search implementation
    Takes the undirected graph #ugraph and the node #start_node
    Returns the set consisting of all nodes that are visited
    by a breadth-first search that starts at start_node.
    """
    queue = Queue()
    visited = set()
    visited.add(start_node)
    queue.enqueue(start_node)
    while not queue.is_empty():
        node = queue.dequeue()
        for neighbor in ugraph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)

    return visited


def cc_visited(ugraph):
    """
    Compute connected components
    Takes the undirected graph #ugraph
    Returns a list of sets, where each set consists of all
    the nodes in a connected component, and there is exactly
    one set in the list for each connected component in ugraph and nothing else.
    """
    remaining_nodes = set(ugraph.get_nodes())
    connected_components = list()
    while remaining_nodes:
        node = random.choice(list(remaining_nodes))
        visited = bfs_visited(ugraph, node)
        connected_components.append(visited)
        remaining_nodes.difference_update(visited)

    return connected_components


def largest_cc_size(ugraph):
    """Takes the undirected graph #ugraph.
    Returns the size (an integer) of the largest connected component in ugraph.
    """
    connected_components = cc_visited(ugraph)
    if len(connected_components) == 0:
        return 0
    return len(sorted(connected_components, key=len, reverse=True)[0])


def compute_resilience(ugraph, attack_order):
    """Takes the undirected graph #ugraph, a list of nodes #attack_order
    For each node in the list, the function removes the given node and its edges
    from the graph and then computes the size of the largest connected component
    for the resulting graph.
    Returns a list whose k+1th entry is the size of the largest connected component
    in the graph after the removal of the first k nodes in attack_order.
    The first entry (indexed by zero) is the size of the largest connected component
    in the original graph.
    """
    ugraph = ugraph.copy()
    cc_lst = list()
    for node in attack_order:
        cc_lst.append(largest_cc_size(ugraph))
        del ugraph[node]

    cc_lst.append(largest_cc_size(ugraph))
    return cc_lst


def random_order(graph):
    nodes = list(graph.get_nodes())
    random.shuffle(nodes)
    return nodes


def fast_targeted_order(graph):
    graph = graph.copy()
    graph_length = len(graph)
    degree_sets = {}
    for k in range(graph_length):
        degree_sets[k] = set([])

    degrees = graph.in_degrees()
    for i in range(graph_length):
        d = degrees[i]
        degree_sets[d].add(i)

    order = []
    i = 0
    for k in range(graph_length - 1, -1, -1):
        while degree_sets[k]:
            degrees = graph.in_degrees()
            node = degree_sets[k].pop()
            for neighbor in graph[node]:
                degrees = graph.in_degrees()
                d = degrees[node]
                degree_sets[d].remove(neighbor)
                degree_sets[d - 1].add(neighbor)
            order[i] = node
            i += 1
            del graph[node]
    return order


def targeted_order(graph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = graph.copy()
    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


nodes, edges = load_graph_data('alg_rf7.txt')
num_nodes = len(nodes)

# Computer Network graph
comp_net_graph = Graph(nodes, edges)

# Erdos and Renyi graph
er_graph = ER(num_nodes, .002)

# Preferential Attachment graph
pa_graph = Graph()
pa_graph.make_complete(3)
trials = UPATrial(3)
for node in range(3, num_nodes):
    new_nodes = trials.run_trial(3)
    pa_graph[node] = new_nodes


def main():

    # comp_attack_order = random.sample(random_order(comp_net_graph), 240)
    # er_attack_order = random.sample(random_order(er_graph), 240)

    # comp_attack_order = random_order(comp_net_graph)
    # er_attack_order = random_order(er_graph)
    # pa_attack_order = random_order(pa_graph)


    # comp_resilience = compute_resilience(comp_net_graph, comp_attack_order)
    # er_resilience = compute_resilience(er_graph, er_attack_order)
    # pa_resilience = compute_resilience(pa_graph, pa_attack_order)

    # plt.plot(comp_resilience, color='blue', label='Computer Network')
    # plt.plot(er_resilience, color='red', label='Erdos and Renyi random graph')
    # plt.plot(pa_resilience, color='green', label='Undirected Preferential Attachment graph')

    # plt.title('Resilience of different graphs', fontsize=18, color='#ff8800')
    # plt.xlabel('Number of nodes removed', fontsize=14, color='#ff8800')
    # plt.ylabel('Size of the largest connected component', fontsize=14, color='#ff8800')
    # plt.legend(loc='best', labels=['Computer Network',
    #                                'Erdos and Renyi random graph',
    #                                'Undirected Preferential Attachment graph'])
    # plt.show()

    print(len(comp_net_graph), comp_net_graph.get_num_edges(), largest_cc_size(comp_net_graph))
    print(len(er_graph), er_graph.get_num_edges(), largest_cc_size(er_graph))
    print(len(pa_graph), pa_graph.get_num_edges(), largest_cc_size(pa_graph))


if __name__ == '__main__':
    main()
