class Edge:
    def __init__(self, source, target, label=None, attributes=None):
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
