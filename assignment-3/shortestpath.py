# Stefanos Iordanis Iosifidis 2705
from heapq import heapify, heappush, heappop
from sys import argv
from math import sqrt, inf

class Node:
    def __init__(self, id, coords):
        self.id = id
        self.x = coords[0]
        self.y = coords[1]
        self.neighboors = []

    def add_neighboor(self, neighboor, distance):
        self.neighboors.append([neighboor, distance])

    def find_distance(self, other):
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)

        return sqrt(dx**2 + dy**2)

    def visit(self):
        self.is_visited = True

    def __lt__(self, other):
        return self.SPD < other.SPD

# Find the shortest path with Dijkstra's algorithm
def dijkstra(graph, source_id, target_id):

    for v in graph:
        v.SPD = inf # Initialize shortest distance from s to all nodes
        v.path = [] # Initialize shortest path from s to all nodes
        v.is_visited = False

    pq = [] # Initialize the priority queue
    s = graph[int(source_id)]
    s.SPD, s.path = 0, [s.id]
    heappush(pq, (0, s))
    it = 0
    # While priority queue is not empty
    while pq:
        v = heappop(pq)
        v = v[1]
        v.visit()
        it += 1
        if v.id == int(target_id):
            return (it, v)

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

# Find the shortest path with A*-search
def astar(graph, source_id, target_id):

    for v in graph:
        v.SPD = inf # Initialize shortest distance from s to all nodes
        v.path = [] # Initialize shortest path from s to all nodes
        v.is_visited = False

    pq = [] # Initialize the priority queue
    t = graph[int(target_id)]
    s = graph[int(source_id)]
    s.SPD, s.path = 0, [s.id]
    heappush(pq, (None, s))
    it = 0
    # While priority queue is not empty
    while pq:
        v = heappop(pq)
        v = v[1]
        v.visit()
        it += 1
        if v.id == int(target_id):
            return (it, v)

        for node in v.neighboors:
            u = graph[node[0]]
            weight = node[1]
            if u.is_visited == False:
                if u.SPD > v.SPD + weight:
                    u.SPD = v.SPD + weight
                    u.path = v.path + [u.id]
                    pq = [x for x in pq if x[1].id != u.id]
                    heapify(pq)
                    heappush(pq, (u.SPD + u.find_distance(t), u))

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

#
if __name__ == '__main__':

    graph = parse_graph(argv[1])

    (it, t) = dijkstra(graph, argv[2], argv[3])
    print("Dijkstra:")
    print("Shortest path length = {}\nShortest path distance = {}".format(len(t.path), t.SPD))
    print("Shortest path: {}".format(t.path), end=' ')
    print("\nnumber of visited nodes = {}".format(it))

    (it, t) = astar(graph, argv[2], argv[3])
    print("\nA*:")
    print("Shortest path length = {}\nShortest path distance = {}".format(len(t.path), t.SPD))
    print("Shortest path: {}".format(t.path), end=' ')
    print("\nnumber of visited nodes = {}".format(it))
