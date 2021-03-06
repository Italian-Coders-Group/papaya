from typing import Dict, Any, List, Tuple, Union

from core.abc.database.backend import AbstractBackend
from core.abc.database.database import AbstractDatabase
from core.database.backend import SqlBackend
from core.database.guild import Guild

import itertools


_tables: Dict[str, List[str] ] = {
	'users': [
		'guildID',
		'discordID',
		'personalPrefix',
		'permissions'
	],
	'games': [
		'guildID',
		'gameID',
		'gameType',
		'userIDs',
		'gameData',
		'live'
	],
	'stats': [
		'guildID',
		'userID',
		'gameType',
		'wins',
		'losses',
		'ties'
	],
	'ranks': [
		'rank',
		'minPoints',
		'maxPoints'
	],
	'gameTypes': [
		'gameType'
	],
	'gameRequests': [
		'userID',
		'user2ID',
		'guildID',
		'channelID',
		'gameType'
	]
}


class Database(AbstractDatabase):

	_cache: Dict[int, Guild] = {}
	instance: 'Database'
	backend: AbstractBackend

	def __init__( self ):
		self.backend = SqlBackend('../resources/database.db')
		Database.instance = self

	def getGuild( self, guild: int ) -> Guild:
		"""
		Returns a Guild object for interacting with the database
		:param guild: guid ID
		:return: the Guild Object
		"""
		if guild not in self._cache.keys():
			self._cache[guild] = Guild(guild, self)
		return self._cache.get(guild)

	def makeRequest( self, sql: str, *args, convertSingle: bool = True, table: str = '' ) -> Union[ List[ Dict[str, Any] ], Dict[str, Any] ]:
		"""
		Makes a request with SQL code to the database.
		DO NOT USE VARIABLES IN THE SQL CODE!
		IS **VERY** INSECURE AND CAN CAUSE DATA LOSS!
		:param table: the table this request operates on
		:param convertSingle: def True, if True when a result list has a single item, extract it from the list and return it
		:param sql: SQL code
		:param args: arguments for value sanitizing
		:return: a List with the result (can be emtpy)
		"""
		if table == '':
			return _fromTupleListToList(self.backend.makeRequest(sql, *args))

		return _makeDictionary( table, self.backend.makeRequest(sql, *args) )

	def makeUniqueRequest(self, sql: str, *args, convertSingle: bool = True, table: str = '') -> Union[ List[ Dict[str, Any] ], Dict[str, Any] ]:
		"""
		Makes a request with SQL code to the database.
		DO NOT USE VARIABLES IN THE SQL CODE!
		IS **VERY** INSECURE AND CAN CAUSE DATA LOSS!
		:param convertSingle:
		:param table:
		:param sql: SQL code
		:param args: arguments for value sanitizing
		:return: a Single Object with the result (can be emtpy)
		"""
		if table == '':
			return _fromTupleToList(self.backend.makeUniqueRequest(sql, *args))

		return _makeUniqueDictionary( table, self.backend.makeUniqueRequest(sql, *args))

	def save( self ) -> None:
		"""	Commit changes to the database file	"""
		if getattr(self, 'backend', None) is not None:
			self.backend.save()

	def __del__( self ):
		# save when closing!
		self.save()


def _makeDictionary( table: str, row: List[Tuple] ) -> List[ Dict[str, Any] ]:
	items: List[ Dict[str, Any] ] = []
	for item in row:
		if table in _tables.keys():
			template = _tables[table]  # get the dictionary template from the known tables
			items.append(
				{
					# associate a key with a value
					template[pos]: value for pos, value in enumerate(item)
				}
			)
		else:
			items.append( { pos: value for pos, value in enumerate(item) } )

	return items


def _makeUniqueDictionary( table: str, queryResult: Any) -> Dict[str, Any]:
	if table in _tables.keys():
		template = _tables[table]

		dictionary = {
			template[pos]: value for pos, value in enumerate(queryResult)
		}
	else:
		return {pos:  value for pos, value in enumerate(queryResult)}
	return dictionary


def _fromTupleListToList(myTuple: List[Tuple]) -> List:
	return list(itertools.chain(*myTuple))


def _fromTupleToList(myTuple: Tuple) -> List:
	out = []
	for value in myTuple:
		out.append(value)
	return out