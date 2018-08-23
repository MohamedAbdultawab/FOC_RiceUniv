#!/usr/bin python3.5
"""
   Module 2
   Implementation of breadth-first search.
   A function to compute the set of connected components (CCs) of an undirected graph
   A function to determine the size of its largest connected component.
   A function to computes the resilience of a graph (measured by the size of its largest connected component)
   as a sequence of nodes are deleted from the graph.
"""
from collections import deque, Counter
from random import choice


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
    while len(remaining_nodes) != 0:
        node = choice(list(remaining_nodes))
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
    cc_lst = list()
    for node in attack_order:
        cc_lst.append(largest_cc_size(ugraph))
        del ugraph[node]
        for key in ugraph:
            for value in ugraph[key]:
                if value == node:
                    ugraph[key].remove(node)
                    break

    cc_lst.append(largest_cc_size(ugraph))
    return cc_lst


def test_bfs():
    graph = dict()
    graph[0] = set([1, 2])
    graph[1] = set([0, 4])
    graph[2] = set([0, 4])
    graph[3] = set([])
    graph[4] = set([1, 2])

    print(bfs_visited(graph, 0) == set([0, 1, 2, 4]))
    print(bfs_visited(graph, 3) == set([3]))


def test_queue():
    q1 = Queue([])
    q1.enqueue(7)
    q1.enqueue(8)
    q1.enqueue(9)
    q1.enqueue(10)
    print(q1)
    print(len(q1))
    print(q1.is_empty())
    q1.clear()
    print(q1.is_empty())
    print(q1)


def test_cc():
    graph = dict()
    graph[0] = set([1, 2, 3])
    graph[1] = set([0, 3, 4])
    graph[2] = set([0, 4])
    graph[3] = set([0, 1])
    graph[4] = set([1, 2])
    graph[5] = set([])
    graph[6] = set([7])
    graph[7] = set([6])

    print(largest_cc_size(graph) == 5)


if __name__ == '__main__':
    test_queue()
    test_bfs()
    test_cc()
