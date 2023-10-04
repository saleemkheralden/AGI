from Memory.Node import Node
from Memory.Edge import Edge
import networkx as nx
import matplotlib.pyplot as plt

class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def remove_node(self, node):
        if node.id in self.nodes.keys():
            del self.nodes[node.id]

    def get_node(self, node_id):
        if node_id in self.nodes.keys():
            return self.nodes[node_id]
        return None

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def get_all_nodes(self):
        return list(self.nodes)

    def get_all_edges(self):
        return self.edges

    def visualize(self):
        graph = nx.Graph()

        for edge in self.edges:
            graph.add_node(str(edge.source))
            graph.add_node(str(edge.target))
            graph.add_edge(str(edge.source), str(edge.target))

        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True)
        plt.show()



