from Memory.KnowledgeGraph import KnowledgeGraph
from Memory.Node import Node
from Memory.Edge import Edge
from hashlib import sha3_512 as sha


alpha = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
words = ['apple', 'banana', 'dad', 'mom']

def hash(str):
    return sha(f'{str}'.encode('utf-8')).hexdigest()

kg = KnowledgeGraph()

prev_node = None
for letter in alpha:
    node = Node(id=hash(letter), label=letter)
    kg.add_node(node)

    if prev_node is not None:
        kg.add_edge(Edge(id=hash(f"{node.id}{prev_node.id}"),
                         source=prev_node,
                         target=node))

    prev_node = node


prev_node = None
for digit in digits:
    node = Node(id=hash(digit), label=digit)
    kg.add_node(node)

    if prev_node is not None:
        kg.add_edge(Edge(id=hash(f"{node.id}{prev_node.id}"),
                         source=prev_node,
                         target=node))

    prev_node = node

for word in words:
    node = Node(id=hash(word), label=word)
    kg.add_node(node)

    for letter in word:
        letter_node = kg.get_node(hash(letter))
        kg.add_edge(Edge(id=hash(f"{node.id}{letter_node.id}"),
                         source=node,
                         target=letter_node))


kg.pyvis()



