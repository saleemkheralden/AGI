from Memory.MemoryUnit import MemoryUnit
import numpy as np

class Edge(MemoryUnit):

    def __init__(self,
                 id,
                 source, target,
                 str_score=0.,
                 str_decay_factor=0.,
                 # label=None,
                 # attributes=None):
                 ):

        super(Edge, self).__init__(id=id,
                                   str_score=str_score,
                                   str_decay_factor=str_decay_factor)
        self.source = source
        self.target = target
        # self.label = label
        # self.attributes = attributes if attributes is not None else {}

    # def add_attribute(self, key, value):
    #     self.attributes[key] = value
    #
    # def remove_attribute(self, key):
    #     if key in self.attributes.keys():
    #         del self.attributes[key]
    #
    # def get_attribute(self, key):
    #     return self.attributes.get(key, None)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"(id:{self.id},source:{self.source},target:{self.target},str_score:{self.str_score})"
