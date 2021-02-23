from abc import ABCMeta, abstractmethod


class BaseGame(metaclass=ABCMeta):

	@abstractmethod
	async def processTurn( self ):
		pass