from Memory.Node import Node
from Memory.Edge import Edge
import networkx as nx
import matplotlib.pyplot as plt
# import json
from pyvis.network import Network
# from hashlib import sha3_512 as sha
from threading import Thread
from time import sleep
import socket
from queue import Queue
from server_commands import cmd, string_delim, obj

class KnowledgeGraph:
    def __init__(self, connect_ui=True):
        self.nodes = {}
        self.edges = []  # might be removed
        self.neigh_matrix = {}
        self.connect_ui = connect_ui

        self.updates_queue = Queue()

        if self.connect_ui:
            self.server_status = True
            self.server_ip = "0.0.0.0"
            self.server_port = 45000
            self.th = Thread(target=self.server)
            self.th.start()


    def server(self):
        addr = (self.server_ip, self.server_port)
        print(addr)
        recv_size = 2048
        i = 0

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(addr)
        print("server bind")

        while self.server_status:
            server_socket.listen()
            print("server listening")

            client_socket, client_addr = server_socket.accept()
            client_socket.settimeout(1)
            msg = None

            with client_socket:
                flag = False
                while msg != cmd.SHUTDOWN:
                    try:
                        msg = client_socket.recv(recv_size)
                        msg = msg.decode()
                        print(f"{client_addr}> {msg}")

                        if msg == cmd.INIT.value:
                            flag = True
                            print("sending init")
                            for node in self.nodes.values():
                                print(f"sending {node}")
                                client_socket.sendall(f"{cmd.ADD.value}{string_delim.COMMAND_TYPE.value}"
                                                   f"{obj.NODE.value}{string_delim.OBJECT_TYPE.value}{node}".encode("utf-8"))
                                sleep(1)
                            for edge in self.edges:
                                print(f"sending {edge}")
                                client_socket.sendall(f"{cmd.ADD.value}{string_delim.COMMAND_TYPE.value}"
                                                   f"{obj.EDGE.value}{string_delim.OBJECT_TYPE.value}{edge}".encode("utf-8"))
                                sleep(1)

                    except socket.timeout as e:
                        msg = None
                    except Exception as e:
                        break

                    if flag and (not self.updates_queue.empty()):
                        client_socket.sendall(self.updates_queue.get().encode("utf-8"))
                    sleep(1)

                client_socket.close()


    def add_node(self, node: Node):
        self.nodes[node.id] = node
        self.updates_queue.put(f"{cmd.ADD.value}{string_delim.COMMAND_TYPE.value}"
                               f"{obj.NODE.value}{string_delim.OBJECT_TYPE.value}{node}")

    def remove_node(self, node):
        if node.id in self.nodes.keys():
            self.updates_queue.put(f"{cmd.REMOVE.value}{string_delim.COMMAND_TYPE.value}"
                                   f"{obj.NODE.value}{string_delim.OBJECT_TYPE.value}{node}")
            del self.nodes[node.id]

    def get_node(self, node_id):
        if node_id in self.nodes.keys():
            return self.nodes[node_id]
        return None

    def add_edge(self, source, target):
        _edge = Edge(id=hash(f"{source.id}{target.id}"),
                           source=source,
                           target=target)
        self.add_edge(_edge)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        edge.source.add_conn(edge)

        if edge.source.id not in self.neigh_matrix:
            self.neigh_matrix[edge.source.id] = {}
        self.neigh_matrix[edge.source.id][edge.target.id] = edge.str_score

        self.updates_queue.put(f"{cmd.ADD.value}{string_delim.COMMAND_TYPE.value}"
                               f"{obj.EDGE.value}{string_delim.OBJECT_TYPE.value}{edge}")


    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
        if edge.target.id in self.neigh_matrix[edge.source.id]:
            self.neigh_matrix[edge.source.id].pop(edge.target.id)
        edge.source.remove_conn(edge)
        self.updates_queue.put(f"{cmd.REMOVE.value}{string_delim.COMMAND_TYPE.value}"
                               f"{obj.EDGE.value}{string_delim.OBJECT_TYPE.value}{edge}")

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


    def pyvis(self):
        net = Network(
            notebook=True,

            select_menu=True,
            filter_menu=True
        )

        # node_keys = list(self.nodes.values())
        node_keys = [str(e.label) for e in self.nodes.values()]

        net.add_nodes(node_keys, label=list(map(str, self.nodes.values())))
        net.add_node(60, shape="image", image="https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg", label="cat")

        net.add_edges([(int(e.source.label) if e.source.label.isdigit() else e.source.label,
                        int(e.target.label) if e.target.label.isdigit() else e.target.label)
                       for e in self.edges])

        net.show("KnowledgeGraph.html")
        return net




