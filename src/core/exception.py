class ChannelNotFoundException(Exception):
	"""	This exception is raised if a channel isn't found """
	pass


class OperationNotSupportedException(Exception):
	"""	This exception is raised if an operation isn't supported on an object/function for a parameter type """
	pass


class FileSystemError(OperationNotSupportedException):
	""" This exception is raised by FileSystem methods """
	pass
