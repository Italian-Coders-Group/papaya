from abc import ABCMeta, abstractmethod

from core.types import Event, Coroutine


class AbstractEventSystem(metaclass=ABCMeta):

	@abstractmethod
	def removeListeners( self, module: str ):
		pass

	@abstractmethod
	def addListener( self, listener: Coroutine, event: Event ):
		pass
