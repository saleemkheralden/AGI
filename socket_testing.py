from Memory.KnowledgeGraph import KnowledgeGraph
from Memory.Node import Node
from time import sleep

kg = KnowledgeGraph(connect_ui=True)

node = Node(id="000000001",
			label="cat picture",
			type="image",
			encoding=[0.1, 0, 5],
			str_score=1.7,
			str_decay_factor=0.8)

node2 = Node(id="000000002",
			label="dog picture",
			type="image",
			encoding=[0.8, 1, 4.1],
			str_score=3.2,
			str_decay_factor=0.152)



kg.add_node(node)
print(kg.updates_queue.queue)

sleep(5)

kg.add_node(node2)
print(kg.updates_queue.queue)




msg = ""
while msg != "QUIT":
	msg = input("msg")

	id = input("id: ")
	label = input("label: ")
	type = input("type: ")
	kg.add_node(Node(id=id,
					 label=label,
					 type=type,
					 encoding=[0] * 3,
					 str_score=0,
					 str_decay_factor=0.7))
	print(kg.updates_queue.queue)



kg.server_status = False



