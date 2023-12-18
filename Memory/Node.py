from Memory.MemoryUnit import MemoryUnit
import numpy as np

class Node(MemoryUnit):

    def __init__(self,
                 id,
                 label=None, # label is a text explanation of the node
                 type=None, # type can be: image, text, audio ...
                 encoding=None,
                 str_score=0,
                 str_decay_factor=0,
                 # att_score=0,
                 # att_decay_factor=0,
                 # attributes=None):
                 ):

        super(Node, self).__init__(id=id,
                                   str_score=str_score,
                                   str_decay_factor=str_decay_factor)

        self.label = label
        self.type = type
        self.encoding = encoding

        self.conn = {}

        # self.att_score = att_score
        # self.att_decay_factor = att_decay_factor

        # self.attributes = attributes if attributes is not None else {}

    # def add_attribute(self, key, value):
    #     self.attributes[key] = value

    # def remove_attribute(self, key):
    #     if key in self.attributes.keys():
    #         del self.attributes[key]

    # def get_attribute(self, key):
    #     return self.attributes.get(key, None)

    def add_conn(self, edge):
        self.conn[edge.target.id] = edge

    def remove_conn(self, edge):
        if edge.target.id in self.conn:
            del self.conn[edge.target.id]

    def __repr__(self):
        id_str = str(self.id)
        if len(id_str) > 5:
            id_str = f"{id_str[:3]}...{id_str[-3:]}"
        return f"MemoryNode(ID: {id_str}, Label: {self.label})"

    def __str__(self):
        return f"({self.id},{self.type},{self.label},{self.str_score})"








