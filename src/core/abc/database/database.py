from abc import ABCMeta, abstractmethod
from typing import List, Any, Dict

from core.database.backends import AbstractBackend


class AbstractDatabase(metaclass=ABCMeta):

	backend: AbstractBackend

	@abstractmethod
	def getGuild( self, guild: int ) -> 'AbstractGuild':
		pass

	def __del__(self):
		self.backend.save()
