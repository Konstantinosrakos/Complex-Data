# Stefanos Iordanis Iosifidis 2705
from heapq import heapify, heappush, heappop
from sys import argv
from math import inf

class Node:
    def __init__(self, id, coords):
        self.id = id
        self.x = coords[0]
        self.y = coords[1]
        self.neighboors = []
        self.current = []
        self.SPD = []
        self.path = []

    def add_neighboor(self, neighboor, distance):
        self.neighboors.append([neighboor, distance])

    def visit(self):
        self.is_visited = True

    def __lt__(self, other):
        return self.SPD < other.SPD

# Find the shortest path with Dijkstra's algorithm
def dijkstra(graph, source_id):

    for v in graph:
        v.SPD = inf # Initialize shortest distance from s to all nodes
        v.path = [] # Initialize shortest path from s to all nodes
        v.is_visited = False

    pq = [] # Initialize the priority queue
    s = graph[int(source_id)]
    s.SPD, s.path = 0, [s.id]
    heappush(pq, (0, s))
    # While priority queue is not empty
    while pq:
        v = heappop(pq)
        v = v[1]
        v.visit()

        yield v

        for n in v.neighboors:
            u = graph[n[0]]
            weight = n[1]
            if u.is_visited == False:
                if u.SPD > v.SPD + weight:
                    u.SPD = v.SPD + weight
                    u.path = v.path + [u.id]
                    # Update/create u
                    pq = [x for x in pq if x[1].id != u.id]
                    heapify(pq)
                    heappush(pq, (u.SPD, u))

# Parse the graph created in the previous part of this assignment
def parse_graph(filename):

    graph = []
    with open(filename, 'r') as fgraph:
        for line in fgraph:
            n = line.split()
            node = Node(int(n[0]), (float(n[1]), float(n[2])))
            for i in range (3, len(n), 2):
                node.add_neighboor(int(n[i]), float(n[i+1]))
            graph.append(node)

    return graph

if __name__ == '__main__':

    graph = parse_graph(argv[1])

    # Gather the requested nodes' ids for the TK search
    clique_ids = [int(argv[x]) for x in range(2,len(argv))]

    # Nodes which correspond to the given clique_ids
    clique = [graph[i] for i in clique_ids]

    # Create the generators for each node of the clique
    for n in clique:
        n.gen = dijkstra(graph, n.id)

    while 1:
        n = min(clique, key=lambda x: x.SPD)
        n.current = next(n.gen)

        if all(n.current.id in c.path for c in clique):
            print(1)
            break
        