class ChannelNotFoundException(Exception):
	"""	This exception is raised if a channel isn't found """
	pass


class OperationNotSupportedException(Exception):
	"""	This exception is raised if an operation isn't supported on an object/function for a parameter type """
	pass


class FileSystemError(OperationNotSupportedException):
	""" This exception is raised by FileSystem methods """
	pass


class GameNotFound(Exception):
	""" This exception is raised when a game is not found """
	pass


class GameRequestAlreadyLive(Exception):
	""" This exception is raised if someone has a request ongoing """
	pass


class GameRequestNotFound(Exception):
	""" This exception is raised if a gamerequest is not found """
	pass