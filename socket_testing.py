from Memory.KnowledgeGraph import KnowledgeGraph
from Memory.Node import Node
from Memory.Edge import Edge
from time import sleep
from server_commands import cmd

kg = KnowledgeGraph(connect_ui=True)

node = Node(id="000000001",
			label="cat picture",
			type="image",
			encoding=[0.1, 0, 5],
			str_score=1.,
			str_decay_factor=0.8)

node2 = Node(id="000000002",
			label="dog picture",
			type="image",
			encoding=[0.8, 1, 4.1],
			str_score=0.4,
			str_decay_factor=0.152)

edge12 = Edge(id="000000001",
			  source=node,
			  target=node2,
			  str_score=0.8,
			  str_decay_factor=0.4)


kg.add_node(node)
print(kg.updates_queue.queue)

sleep(5)

kg.add_node(node2)
print(kg.updates_queue.queue)

sleep(2)
kg.add_edge(edge=edge12)
print(kg.updates_queue.queue)


msg = ""
while True:
	msg = input("msg")
	if msg == "exit":
		break

	id = input("id: ")
	label = input("label: ")
	type = input("type: ")
	score = input("score: ")
	kg.add_node(Node(id=id,
					 label=label,
					 type=type,
					 encoding=[0] * 3,
					 str_score=float(score),
					 str_decay_factor=0.7))
	print(kg.updates_queue.queue)



kg.server_status = False



