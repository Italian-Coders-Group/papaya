from typing import Dict, Any, List, Tuple, Union

from core.abc.database.backend import AbstractBackend
from core.abc.database.database import AbstractDatabase
from core.database.backend import SqlBackend
from core.database.guild import Guild


_tables: List[str] = [
	'games',
	'users',
	'stats',
	'ranks',
	'gameTypes',
	'accepts'
]


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
		return _makeDictionary( table, self.backend.makeRequest(sql, *args), convertSingle )

	def save( self ) -> None:
		"""	Commit changes to the database file	"""
		if self.backend is not None:
			self.backend.save()

	def __del__( self ):
		# save when closing!
		self.save()


def _makeDictionary(table: str, row: List[Tuple], convertSingle: bool) -> Union[ List[ Dict[str, Any] ], Dict[str, Any] ]:
	items: List[ Dict[str, Any] ] = []
	for item in row:
		if table == 'games':
			items.append(
				{
					'guildID': item[ 0 ],
					'gameID': item[ 1 ],
					'gameType': item[ 2 ],
					'userIDs': item[ 3 ],
					'gameData': item[ 4 ],
					'live': item[ 5 ]
				}
			)
		elif table == 'users':
			items.append(
				{
					'guildID': item[ 0 ],
					'discordID': item[ 1 ],
					'personalPrefix': item[ 2 ],
					'permissions': item[ 3 ]
				}
			)
		elif table == 'stats':
			items.append(
				{
					'guildID': item[ 0 ],
					'userID': item[ 1 ],
					'gameType': item[ 2 ],
					'wins': item[ 3 ],
					'losses': item[ 4 ],
					'ties': item[ 5 ]
				}
			)
		elif table == 'ranks':
			items.append(
				{
					'rank': item[ 0 ],
					'minPoints': item[ 1 ],
					'maxPoints': item[ 2 ]
				}
			)
		elif table == 'gameTypes':
			items.append(
				{
					'gameType': item[ 0 ]
				}
			)
		elif table == 'gameRequests':
			items.append(
				{
					'userID': item[ 0 ],
					'user2ID': item[ 1 ],
					'guildID': item[ 2 ],
					'channelID': item[ 3 ]
				}
			)
		else:
			items.append( { pos: value for pos, value in enumerate(item) } )

	if convertSingle and len(items) == 1:
		return items[0]
	return items
