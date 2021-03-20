from types import FunctionType
from typing import Dict, Union

from botframework.abc.eventSystem import AbstractEventSystem
from botframework.logging import get_logger
from botframework.types import ListenerList, Event, Coroutine

logger = get_logger('EventSystem')


class Events:
	ReactionAdded = 'ReactionAdded'.lower()
	ReactionRemoved = 'ReactionRemoved'.lower()
	MessageArrived = 'message'
	Reload = 'reload'


class EventSystem(AbstractEventSystem):

	INSTANCE: 'EventSystem'
	_listeners: Dict[ Event, ListenerList ]

	def __init__(self):
		EventSystem.INSTANCE = self

	def removeListeners( self, module: str ):
		# cycle in all event lists
		for listenerList in self._listeners.values():
			toRemove = []
			for listener in listenerList:
				if listener.__module__ == module:
					toRemove.append( listener )  # schedule for removal all listeners of module module
			for func in toRemove:
				listenerList.remove(func)  # remove all found listeners

	def addListener( self, listener: Coroutine, event: Event ):
		# check if the event list exists
		if event not in self._listeners.keys():
			# if not, create it
			self._listeners[ event ] = [ ]
		# add the listener
		logger.info( f'Module "{listener.__module__}" registered listener for event "{event}".' )
		self._listeners[ event ].append( listener )
		return listener

	async def invoke( self, event: Union[Event, Events], **kwargs ):
		"""
		Invoke an event, calling all listeners that are listening for it, with the given kwargs.
		:param event: event to trigger
		:param kwargs: listener parameters
		"""
		if event not in self._listeners.keys():
			self._listeners[ event ] = []

		if len( self._listeners[event ] ) == 0:
			logger.warning(f'Invoked event "{event}" has no _listeners!')

		for listener in self._listeners[event ]:
			try:
				await listener(**kwargs)
			except Exception as e:
				logger.error(
					f'Caught error for listener "{listener.__name__}" from module "{listener.__module__}" while invoking event {event}',
					exc_info=e
				)


EventSystem()


# event listeners should be named:
# onEventName

def Listener(*args: Union[str, FunctionType], **kwargs):
	"""
	Decorator for event listeners.
	listeners should be named after the event they are listening for, ex:

	@Listener
	async def onMessage(server: AbstractServer, msg: Message):
		pass

	if this is not possible, an event parameter can be passed to the decorator to set it,
	"""
	# check if called without parameters
	if len( args ) > 0 and type( args[0] ) == FunctionType:
		# add the listener with even from func name
		return EventSystem.INSTANCE.addListener( args[0], args[0].__code__.co_name[2:].lower() )

	# called with parameter, get it
	event: str = kwargs.get( 'event' ) if 'event' in kwargs else args[0]

	# add the listener
	return lambda func: EventSystem.INSTANCE.addListener(func, event)
