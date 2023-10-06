from Memory.MemoryUnit import MemoryUnit
class Edge(MemoryUnit):

    def __init__(self,
                 id,
                 source, target,
                 imp_score=.0,
                 imp_spike_factor=.0,
                 imp_spike_add=.0,
                 imp_decay_factor=.0,
                 core_thresh=.0,
                 ob_thresh=.0,

                 act_score=.0,
                 act_decay_factor=.0,
                 label=None,
                 attributes=None):

        super(Edge, self).__init__(imp_score=imp_score,
                                   imp_spike_factor=imp_spike_factor,
                                   imp_spike_add=imp_spike_add,
                                   imp_decay_factor=imp_decay_factor,
                                   core_thresh=core_thresh,
                                   ob_thresh=ob_thresh,
                                   act_score=act_score,
                                   act_decay_factor=act_decay_factor)

        self.source = source
        self.target = target
        self.label = label
        self.attributes = attributes if attributes is not None else {}

    def add_attribute(self, key, value):
        self.attributes[key] = value

    def remove_attribute(self, key):
        if key in self.attributes.keys():
            del self.attributes[key]

    def get_attribute(self, key):
        return self.attributes.get(key, None)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Edge(source: {self.source}, target: {self.target})"
