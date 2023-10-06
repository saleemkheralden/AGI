from Memory.Node import Node
from Memory.Edge import Edge
import networkx as nx
import matplotlib.pyplot as plt
import json
import pyvis

class KnowledgeGraph:
    def __init__(self, connect_ui=True):
        self.nodes = {}
        self.edges = []
        self.connect_ui = connect_ui
        if self.connect_ui:
            pass



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


    def d3js_json(self):
        ret = {'nodes': [], 'links': []}

        for node_id, node in self.nodes.items():
            ret['nodes'].append({
                'id': node_id,
                'label': node.label,
                'type': node.type,
                'attributes': node.attributes
            })
        for edge in self.edges:
            ret['links'].append({
                'source': edge.source.id,
                'target': edge.target.id,
                'label': edge.label,
                'attributes': edge.attributes
            })

        return ret






