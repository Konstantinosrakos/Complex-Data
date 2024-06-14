from sys import argv

class Node:
    def __init__(self, id, coords):
        self.id = id
        self.x = coords[0]
        self.y = coords[1]
        self.neighboors = []

    def add_neighboor(self, neighboor, distance):
        self.neighboors.append([neighboor, distance])

# Find the adjacent nodes of each node
def find_neighboors(edges_file, nodes):

    with open(edges_file, 'r') as fedges:
        for edge in fedges:
            z, n1, n2, distance = edge.split()
            nodes[int(n1)].add_neighboor(n2, float(distance))
            nodes[int(n2)].add_neighboor(n1, float(distance))

    return nodes

# Create node objects from input data
def create_nodes(nodes_file):

    with open(nodes_file, 'r') as fnodes:
        nodes_list = []
        for node in fnodes:
            nodeId, x, y = node.split()
            nodes_list.append(Node(nodeId, (x, y)))

    return nodes_list

# Read data from input files
def input_reader(filename1, filename2):

    nodes_list = create_nodes(filename1)

    nodes = find_neighboors(filename2, nodes_list)

    return nodes

# Write data into output file
def output_writer(graph):

    with open("out.txt", 'w') as out:
        for node in graph:
            out.write("{} {} {}".format(node.id, node.x, node.y))
            for n in node.neighboors:
                out.write(" {} {}".format(n[0], n[1]))
            out.write("\n")

#
if __name__ == '__main__':

    # Parse the nodes and their edges and create the graph
    graph = input_reader(filename1=argv[1], filename2=argv[2])

    output_writer(graph)