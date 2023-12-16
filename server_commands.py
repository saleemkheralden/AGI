from enum import Enum

class cmd(Enum):
	SHUTDOWN = "SHUTDOWN"
	UPDATE = "UPDATE"
	ADD = "ADD"
	REMOVE = "REMOVE"

class string_delim(Enum):
	COMMAND_TYPE = "@"
	OBJECT_TYPE = "$"

