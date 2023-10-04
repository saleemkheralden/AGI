
class Node:
    def __init__(self, id, label=None, type=None, attributes=None):
        self.id = id
        self.label = label
        self.type = type
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
        return f"MemoryNode(ID: {self.id}, Label: {self.label})"








