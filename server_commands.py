from enum import Enum

class cmd(Enum):
	INIT = "INIT"
	SHUTDOWN = "SHUTDOWN"
	UPDATE = "UPDATE"
	ADD = "ADD"
	REMOVE = "REMOVE"

class string_delim(Enum):
	COMMAND_TYPE = "@"
	OBJECT_TYPE = "$"
	# OBJECT_DEL = "&"
	DATA_DEL = "#"

class obj(Enum):
	NODE = "Node"
	EDGE = "Edge"

