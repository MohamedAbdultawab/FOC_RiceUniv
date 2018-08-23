#!/usr/bin python3.5
import random
import time
from itertools import chain
import matplotlib.pyplot as plt
from collections import deque
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


def timeit(func, *args, **kwargs):
    start = time.time()
    func(*args, **kwargs)
    return time.time() - start


def make_graph(nodes, edges):
    """Returns a graph from a list of nodes
    and a list of edges represented as tuples"""
    graph = dict()
    for node in nodes:
        graph[node] = set()
    for edge in edges:
        graph[edge[0]].add(edge[1])
    return graph


def remove_node(graph, node):
    for neighbor in graph[node]:
            graph[neighbor].remove(node)
    del graph[node]


def make_complete_graph(num_nodes):
    """Returns a complete graph"""
    nodes = list(range(num_nodes))
    edges = [(node_1, node_2) for node_1 in nodes for node_2 in nodes if node_1 != node_2]
    return make_graph(nodes, edges)


def make_er(num_nodes, probability):
    nodes = list(range(num_nodes))
    edges = list(chain.from_iterable([(i, j), (j, i)]
                 for i in nodes
                 for j in nodes
                 if i != j and random.random() < probability))

    return make_graph(nodes, edges)


def make_upa(num_edges, num_nodes):
    graph = make_complete_graph(num_edges)
    trials = UPATrial(num_edges)

    for node in range(num_edges, num_nodes):
        new_nodes = trials.run_trial(num_edges)
        graph[node] = new_nodes

        for neighbor in new_nodes:
            graph[neighbor].add(node)

    return graph


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
            edges.append((node, int(neighbor))[::-1])

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
    remaining_nodes = set(ugraph.keys())
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
    if not connected_components:
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
    ugraph = deepcopy(ugraph)
    cc_lst = list()
    for node in attack_order:
        cc_lst.append(largest_cc_size(ugraph))
        remove_node(ugraph, node)

    cc_lst.append(largest_cc_size(ugraph))
    return cc_lst


def random_order(graph):
    nodes = list(graph.keys())
    random.shuffle(nodes)
    return nodes


def fast_targeted_order(graph):
    graph = deepcopy(graph)
    graph_length = len(graph)
    degree_sets = [set([]) for degree in range(graph_length)]

    for i in graph.keys():
        d = len(graph[i])
        degree_sets[d].add(i)

    order = []
    for k in range(len(graph) - 1, -1, -1):

        while degree_sets[k]:
            node = degree_sets[k].pop()

            for neighbor in graph[node]:
                d = len(graph[neighbor])
                degree_sets[d].remove(neighbor)
                degree_sets[d - 1].add(neighbor)

            order.append(node)
            remove_node(graph, node)

    return order


def targeted_order(graph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = deepcopy(graph)
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


##################################################
# Application 2 questions
def Q1():

    # Generating graphs
    nodes, edges = load_graph_data('alg_rf7.txt')
    num_nodes = len(nodes)

    # Computer Network graph
    comp_net_graph = make_graph(nodes, edges)

    # Erdos and Renyi graph
    er_graph = make_er(num_nodes, .002)

    # Preferential Attachment graph
    pa_graph = make_upa(3, num_nodes)

    comp_attack_order = random_order(comp_net_graph)
    er_attack_order = random_order(er_graph)
    pa_attack_order = random_order(pa_graph)

    comp_resilience = compute_resilience(comp_net_graph, comp_attack_order)
    er_resilience = compute_resilience(er_graph, er_attack_order)
    pa_resilience = compute_resilience(pa_graph, pa_attack_order)

    plt.figure(figsize=(7, 7), dpi=300)
    plt.plot(comp_resilience, color='blue', label='Computer Network')
    plt.plot(er_resilience, color='green', label='ER random graph')
    plt.plot(pa_resilience, color='red', label='UPA graph')

    plt.title('Resilience of different graphs',
              fontsize=18,
              color='#ff8800')
    plt.xlabel('Number of nodes removed',
               fontsize=14,
               color='#ff8800')
    plt.ylabel('Size of the largest connected component',
               fontsize=14,
               color='#ff8800')
    plt.legend(loc='best', labels=['Computer Network',
                                   'ER random graph, P = .02',
                                   'UPA graph, M = 3'])
    # plt.show()
    plt.savefig('Q1', dpi=300, format='png', transparent=False, orientation='landscape', bbox_inches='tight', pad_inches=0.3)

    # print(len(comp_net_graph), sum([len(x) for x in comp_net_graph.values()]) // 2, largest_cc_size(comp_net_graph))
    # print(len(er_graph), sum([len(x) for x in er_graph.values()]) // 2, largest_cc_size(er_graph))
    # print(len(pa_graph), sum([len(x) for x in pa_graph.values()]) // 2, largest_cc_size(pa_graph))


def Q3():
    """
    fast_targeted_order: fast
    targeted_order: slow
    """
    graph_lengths = range(10, 1000, 10)
    graphs = [make_upa(5, x) for x in graph_lengths]

    fast_times = [timeit(fast_targeted_order, graph) for graph in graphs]
    slow_times = [timeit(targeted_order, graph) for graph in graphs]

    # Plotting

    plt.plot(graph_lengths, fast_times, color='b', label='fast_targeted_order')
    plt.plot(graph_lengths, slow_times, color='g', label='targeted_order')

    plt.title('Regular and fast targeted order - Desktop',
              fontsize=18,
              color='#ff8800')
    plt.xlabel('Size of graph, with M = 5',
               fontsize=14,
               color='#ff8800')
    plt.ylabel('Time in seconds',
               fontsize=14,
               color='#ff8800')
    plt.legend(loc='best', labels=['fast_targeted_order',
                                   'targeted_order'])
    plt.show()
    # plt.savefig('Q3', dpi=300, format='png', transparent=False, orientation='landscape', bbox_inches='tight', pad_inches=0.3)


def Q4():

    # Generating graphs
    nodes, edges = load_graph_data('alg_rf7.txt')
    num_nodes = len(nodes)

    # Computer Network graph
    comp_net_graph = make_graph(nodes, edges)

    # Erdos and Renyi graph
    er_graph = make_er(num_nodes, .002)

    # Preferential Attachment graph
    pa_graph = make_upa(3, num_nodes)

    comp_attack_order = fast_targeted_order(comp_net_graph)
    er_attack_order = fast_targeted_order(er_graph)
    pa_attack_order = fast_targeted_order(pa_graph)

    comp_resilience = compute_resilience(comp_net_graph, comp_attack_order)
    er_resilience = compute_resilience(er_graph, er_attack_order)
    pa_resilience = compute_resilience(pa_graph, pa_attack_order)

    # Plotting
    plt.plot(comp_resilience, color='blue', label='Computer Network')
    plt.plot(er_resilience, color='green', label='ER random graph')
    plt.plot(pa_resilience, color='red', label='UPA graph')

    plt.title('Resilience of different graphs under tageted attacks\nusing fast_targeted_order',
              fontsize=18,
              color='#ff8800')
    plt.xlabel('Number of nodes removed',
               fontsize=14,
               color='#ff8800')
    plt.ylabel('Size of the largest connected component',
               fontsize=14,
               color='#ff8800')
    plt.legend(loc='best', labels=['Computer Network',
                                   'ER random graph, P = .02',
                                   'UPA graph, M = 3'])
    # plt.show()
    plt.savefig('Q4', dpi=300, format='png', transparent=False, orientation='landscape', bbox_inches='tight', pad_inches=0.3)


# print(timeit(Q1))
